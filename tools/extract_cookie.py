#!/usr/bin/env python3
"""Extract the Liftosaur `session` cookie from Chrome into `.liftosaur-session`.

The cookie is httpOnly, so no page script can read it; it has to come out of Chrome's
own cookie store. Chrome encrypts cookie values with a key held in the macOS Keychain,
so the first run pops a Keychain prompt. Click "Always Allow" and later runs are silent.

    python3 tools/extract_cookie.py

Re-run this whenever `tools/liftosaur.py` reports an expired session. That is the entire
maintenance story: one command, no arguments, verifies itself against the live API before
overwriting the existing file.

No third-party packages. Key derivation is stdlib `hashlib`; AES is the `openssl` binary
that ships with macOS.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SESSION_FILE = REPO_ROOT / ".liftosaur-session"
CHROME_DIR = Path.home() / "Library" / "Application Support" / "Google" / "Chrome"

# Chrome's fixed cookie-encryption parameters on macOS. These are constants in Chromium,
# not secrets: the actual secret is the Keychain password fed into PBKDF2.
PBKDF2_SALT = b"saltysalt"
PBKDF2_ITERATIONS = 1003
PBKDF2_KEY_LENGTH = 16
AES_IV = b" " * 16

# The API sits behind a WAF that 403s unrecognised user agents — Python's default gets
# rejected before the cookie is ever looked at. This is not spoofing for access; the
# request is a normal authenticated call from the account's own machine.
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


class ExtractionError(RuntimeError):
    """Anything that stops us producing a verified cookie. Never partially succeeds."""


def read_keychain_password() -> bytes:
    """Chrome's 'Safe Storage' password. Triggers a Keychain prompt on first use."""
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-w", "-s", "Chrome Safe Storage"],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except FileNotFoundError as error:
        raise ExtractionError("`security` not found — this script is macOS-only.") from error
    if result.returncode != 0:
        raise ExtractionError(
            "Could not read 'Chrome Safe Storage' from the Keychain. If a prompt appeared and you "
            "clicked Deny, re-run and choose Allow. Error: " + result.stderr.strip()
        )
    return result.stdout.strip().encode("utf-8")


def find_cookie_databases() -> list[Path]:
    """Every Chrome profile's cookie DB, most-recently-modified first.

    Profiles are `Default`, `Profile 1`, ... — we don't guess which one you signed in with,
    we look in all of them.
    """
    if not CHROME_DIR.exists():
        raise ExtractionError(f"No Chrome data directory at {CHROME_DIR}.")
    databases = [path for path in CHROME_DIR.glob("*/Cookies") if path.is_file()]
    if not databases:
        raise ExtractionError(f"No Cookies database found under {CHROME_DIR}.")
    return sorted(databases, key=lambda path: path.stat().st_mtime, reverse=True)


def read_encrypted_session_cookies(database: Path) -> list[tuple[str, bytes]]:
    """Read liftosaur `session` cookies without disturbing Chrome's live database."""
    with tempfile.TemporaryDirectory() as scratch:
        copy = Path(scratch) / "Cookies"
        shutil.copy2(database, copy)
        connection = sqlite3.connect(f"file:{copy}?immutable=1", uri=True)
        try:
            rows = connection.execute(
                "SELECT host_key, encrypted_value FROM cookies "
                "WHERE name = 'session' AND host_key LIKE '%liftosaur%'"
            ).fetchall()
        finally:
            connection.close()
    return [(host, value) for host, value in rows if value]


def decrypt_cookie_value(encrypted: bytes, password: bytes) -> str:
    if not encrypted.startswith(b"v10"):
        raise ExtractionError(
            f"Unexpected cookie encryption prefix {encrypted[:3]!r}. Chrome changed its scheme; "
            "this script needs updating."
        )
    key = hashlib.pbkdf2_hmac("sha1", password, PBKDF2_SALT, PBKDF2_ITERATIONS, PBKDF2_KEY_LENGTH)
    result = subprocess.run(
        [
            "openssl", "enc", "-d", "-aes-128-cbc", "-nopad",
            "-K", key.hex(),
            "-iv", AES_IV.hex(),
        ],
        input=encrypted[3:],
        capture_output=True,
    )
    if result.returncode != 0:
        raise ExtractionError("openssl failed to decrypt: " + result.stderr.decode(errors="replace").strip())

    plaintext = result.stdout
    if plaintext:  # strip PKCS#7 padding
        padding = plaintext[-1]
        if 1 <= padding <= 16:
            plaintext = plaintext[:-padding]

    # Chrome 127+ prepends a 32-byte SHA-256 domain hash to the plaintext. Older versions
    # don't. Rather than version-sniff, try both and keep whichever is a usable cookie.
    for candidate in (plaintext, plaintext[32:]):
        try:
            text = candidate.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if text.isprintable() and len(text) > 20:
            return text
    raise ExtractionError("Decryption produced no readable cookie — the Keychain password may be wrong.")


def verify_against_api(cookie: str) -> str:
    """A cookie we can't authenticate with is worthless. Prove it works before saving it."""
    request = urllib.request.Request(
        "https://api3.liftosaur.com/api/storage",
        headers={
            "Cookie": f"session={cookie}",
            "Accept": "application/json",
            "User-Agent": BROWSER_USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            import json

            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        if error.code == 401:
            raise ExtractionError(
                "Extracted a cookie but Liftosaur rejected it (401). You are probably signed out in "
                "Chrome — sign in at liftosaur.com, then re-run this."
            ) from error
        if error.code == 403:
            raise ExtractionError(
                "403 from the API. That is the WAF rejecting the request, not a bad cookie — "
                "the User-Agent header is probably missing or has been blocklisted."
            ) from error
        raise ExtractionError(f"Verification request failed: HTTP {error.code}") from error

    email = payload.get("email") or payload.get("storage", {}).get("email")
    if not email:
        raise ExtractionError("Verification succeeded but returned no account email — unexpected response shape.")
    return email


def main() -> int:
    try:
        password = read_keychain_password()

        found: list[tuple[Path, str, bytes]] = []
        for database in find_cookie_databases():
            for host, encrypted in read_encrypted_session_cookies(database):
                found.append((database, host, encrypted))
        if not found:
            raise ExtractionError(
                "No liftosaur `session` cookie in any Chrome profile. Sign in at "
                "https://www.liftosaur.com in Chrome, then re-run this."
            )

        errors = []
        for database, host, encrypted in found:
            try:
                cookie = decrypt_cookie_value(encrypted, password)
                email = verify_against_api(cookie)
            except ExtractionError as error:
                errors.append(f"  {database.parent.name} ({host}): {error}")
                continue

            SESSION_FILE.write_text(cookie + "\n", encoding="utf-8")
            os.chmod(SESSION_FILE, 0o600)
            print(f"wrote {SESSION_FILE} (mode 600)")
            print(f"  profile: {database.parent.name}")
            print(f"  account: {email}")
            print("  verified against GET /api/storage")
            return 0

        raise ExtractionError("Found session cookies but none worked:\n" + "\n".join(errors))

    except ExtractionError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
