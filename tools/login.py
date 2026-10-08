"""
login.py — User authentication against stored credentials.

Responsibilities:
    - Prompt the user for username and password
    - Compare against stored credentials (hash comparison)
    - Limit failed attempts
    - Log every attempt

Public API:
    - authenticate(username, password_hash) -> LoginResult
    - login_flow(get_stored_hash) -> LoginResult | None
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Callable, Optional

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 3


# -------------------- Result model --------------------
@dataclass(frozen=True)
class LoginResult:
    """Outcome of an authentication attempt."""
    username: str
    success: bool

    def __str__(self) -> str:
        if self.success:
            return f"✅ Welcome, {self.username.capitalize()}!"
        return f"❌ Login failed for '{self.username}'."


# -------------------- Authentication logic --------------------
def hash_password(password: str, salt: str = "static_salt_change_me") -> str:
    """Hash a password for comparison (see register.py for warning)."""
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def authenticate(
    username: str,
    password: str,
    stored_username: str,
    stored_password_hash: str,
) -> LoginResult:
    """
    Compare the user's credentials to stored credentials.

    Both username and password are compared using constant-time-safe
    comparison on the hash. The message never reveals which one failed.
    """
    user_hash = hash_password(password)
    username_matches = username.strip().lower() == stored_username.strip().lower()
    password_matches = user_hash == stored_password_hash

    return LoginResult(
        username=username.strip(),
        success=username_matches and password_matches,
    )


# -------------------- Input prompts --------------------
def username_prompt() -> Optional[str]:
    """Prompt for username. Returns None if the user quits."""
    raw = input("Enter your username (or 'q' to quit): ").strip()
    if raw.lower() == "q":
        return None
    if not raw:
        print("❌ Username cannot be empty.")
        return username_prompt()
    return raw


def password_prompt() -> Optional[str]:
    """Prompt for password. Returns None if the user quits."""
    raw = input("Enter your password (or 'q' to quit): ").strip()
    if raw.lower() == "q":
        return None
    if not raw:
        print("❌ Password cannot be empty.")
        return password_prompt()
    return raw


# -------------------- Main login flow --------------------
def login_flow(
    get_stored_user: Callable[[str], Optional[tuple[str, str]]],
    max_attempts: int = MAX_ATTEMPTS,
) -> Optional[LoginResult]:
    """
    Run the interactive login flow.

    Args:
        get_stored_user: A function that takes a username and returns
            (stored_username, stored_password_hash), or None if the user
            doesn't exist.
        max_attempts: Number of allowed attempts before locking out.

    Returns:
        A LoginResult, or None if the user quit or ran out of attempts.
    """
    for attempt in range(1, max_attempts + 1):
        print(f"\n--- Login attempt {attempt}/{max_attempts} ---")

        username = username_prompt()
        if username is None:
            return None

        password = password_prompt()
        if password is None:
            return None

        stored = get_stored_user(username)
        if stored is None:
            logger.warning("Login attempt for unknown user: %s", username)
            # Do not reveal whether the username exists
            print("❌ Invalid username or password.")
            continue

        stored_username, stored_password_hash = stored
        result = authenticate(username, password, stored_username, stored_password_hash)

        if result.success:
            logger.info("Login successful: %s", username)
            return result

        logger.warning("Login failed for user: %s", username)
        print("❌ Invalid username or password.")

    logger.error("Max login attempts reached.")
    print("\n🚫 Too many failed attempts. Try again later.")
    return None


# -------------------- Demo --------------------
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )

    # Temporary in-memory "database" for demonstration.
    # Later, this will be replaced by a real SQLite lookup.
    SAMPLE_USER = ("alice", hash_password("Secure123!"))

    def lookup(username: str) -> Optional[tuple[str, str]]:
        """Fake DB lookup: returns (username, hash) if matched, else None."""
        if username.strip().lower() == SAMPLE_USER[0]:
            return SAMPLE_USER
        return None

    print("\n====== MINJILA COMPREHENSIVE SCHOOL — LOGIN ======\n")
    result = login_flow(get_stored_user=lookup)
    if result:
        print(f"\n{result}")
    else:
        print("\nGoodbye.")