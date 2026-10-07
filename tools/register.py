"""
register.py — User registration with validation and password hashing.

Responsibilities:
  - Prompt the user for name and password
  - Validate name and password
  - Hash the password before returning

Public API:
  - register_user(role: str) -> UserRegistration | None
"""
from __future__ import annotations

import hashlib
import logging
import re
from typing import Optional
from dataclasses import dataclass

#initialize the logger
logger = logging.getLogger(__name__)

#------constants-------
NAME_PATTERN=re.compile(r"^[A-Za-z][A-Za-z\s'\-]{3,24}$")
PASSWORD_MIN_LEN=8
PASSWORD_MAX_LEN=64
VALID_ROLES={"teacher","student"}

#-----Data Model----
@dataclass(frozen=True)
class UserRegistration:
    ''' Immutable record of user registered'''
    name: str
    role: str
    password_hash: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
        if self.role.lower() not in VALID_ROLES:
            raise ValueError(f"Invalid role: {self.role}")

    #customize the output
    def __str__(self) -> str:
        return f"{self.role} '{self.name.capitalize()}' registered successfully"

#Name validation
def validate_name(name:str) -> Optional[str]:
    """
    Validate a person's name.
    Returns None if valid, or an error message if invalid.
    """

    name=name.strip()

    if not name:
        return "Name can't be empty"

    if not NAME_PATTERN.match(name):
        return  "Name must start with a letter, contain only letters, spaces, hyphens, or apostrophes, and be 4–25 characters long."

    return None

def validate_password(password:str) -> Optional[str]:
    """
      Validate a password.
      Rules:
        - 8 to 64 characters
        - At least one letter
        - At least one digit
        - At least one symbol from: !@#$%^&*()-_=+[]{};:'",.<>/?
      Returns None if valid, or an error message if invalid.
      """
    if not (PASSWORD_MIN_LEN <= len(password) <= PASSWORD_MAX_LEN):
        return f"Password must be between {PASSWORD_MIN_LEN} and {PASSWORD_MAX_LEN} characters"

    if not re.search(r"[A-Za-z]", password):
        return "Password must contain at least one letter"

    if not re.search(r"\d", password):
        return "Password must contain at least one digit"

    if not re.search(r"[!@#$%^&*()\-_=+\[\]{};:'\",.<>/?]", password):
        return "Password must contain at least one symbol"

    return None


#hashing the password
def hash_password(password: str,salt:str="static_salt_change_me") -> str:
    """
       Hash a password with SHA-256.

       WARNING: This is for demonstration. In production, use bcrypt or argon2,
       and never use a hardcoded salt.
       """
    return hashlib.sha256((salt+password).encode("utf-8")).hexdigest()

#Get the user name
def name_prompt() -> Optional[str]:
    ''' Prompt the user for name and return None if user quits'''
    while True:
        user_name=input("Please enter your name or q to quit: ").strip()
        if user_name.lower() == "q":
            return None
        error=validate_name(user_name)
        if error is None:
            return user_name
        print(f"{error}")

#get password
def password_prompt() -> Optional[str]:
    ''' Prompt the user for password and return None if user quits'''
    while True:
        user_password=input("Please enter your password or q to quit: ").strip()
        if user_password.lower() == "q":
            return None
        error=validate_password(user_password)
        if error is None:
            return user_password
        print(f"Error: {error}")

#get the role of the user
def role_prompt() -> Optional[str]:
    ''' Prompt the user for role and return None if user quits'''
    while True:
        user_role=input("Please enter your role (teacher or student) or q to quit: ").strip()
        if user_role.lower()=="q":
            return None
        if user_role.lower() in VALID_ROLES:
            return user_role.lower()
        print(f"The role must be one of:{', '.join(sorted(VALID_ROLES))}")

#======================MAIN REGISTRATION FLOW===========================
def register_user(role:Optional[str]=None) -> Optional[UserRegistration]:

    """
       Register a single user.

       Args:
           role: If given, skip the role prompt and use this role.

       Returns:
           A UserRegistration, or None if the user cancelled.
       """
    if role is None:
        role=role_prompt()
        if role is None:
            return None

    name=name_prompt()
    if name is None:
        return None

    password=password_prompt()
    if password is None:
        return None

    registration=UserRegistration(
        name=name,
        role=role.lower(),
        password_hash=hash_password(password)
    )
    logger.info("Registered user %s: %s ",role,name)
    return registration
# ==================== Demo (only runs when file is executed directly) ====================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    print("\n======WELCOME TO MINJILA COMPREHENSIVE SCHOOL REGISTRATION PORTAL======\n")
    while True:
        result=register_user()
        if result is None:
            print("Goodbye!")
            break

        print(result)























































