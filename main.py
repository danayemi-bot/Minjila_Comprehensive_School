"""
main.py — Entry point for the Minjila Comprehensive School CLI.

Responsibilities:
    - Initialize the database
    - Present the top-level menu: Register / Login / Exit
    - Route the user to the correct module based on their choice
    - Only show the dashboard after a successful login

This module is the ONLY place that controls program flow.
All business logic lives in the tools/ package.
"""
from __future__ import annotations

import logging
from typing import Optional


from config import APP_NAME, APP_VERSION, LOG_LEVEL, LOG_FORMAT, LOG_DATE_FORMAT
from tools.sql_storage import init_db, save_user, get_user_by_name
from tools.register import register_user
from tools.login import login_flow, LoginResult
from tools.school_dashboard import show_dashboard


logger = logging.getLogger(__name__)

# -------------------- Helper functions --------------------
def print_header(title: str, width: int = 60) -> None:
    """Print a centered section header."""
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def print_menu() -> None:
    """Print the top-level menu."""
    print_header(f"{APP_NAME} v{APP_VERSION}")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    print("-" * 60)

def ask_choice(prompt: str="Choose option 1-3 :") ->str:
    """Prompt the user for a menu choice."""
    return input(prompt).strip()

# -------------------- Flow functions --------------------
def handle_registration() -> None:
    """Run the registration flow and persist the new user to the DB."""
    print_header("REGISTRATION")

    registration=register_user()
    if registration is None:
        print("Registration cancelled!.")
        return
    #persist the user to DB
    try:
        save_user(
            name=registration.name,
            password_hash=registration.password_hash,
            role=registration.role,
        )
        print(f" {registration}")
    except ValueError as e:
        print(f" {e}")

def handle_login() ->Optional[LoginResult]:
    """
        Run the login flow.

        Returns:
            A LoginResult if login succeeded, else None.
        """
    print_header("LOGIN")

    def lookup(username: str) -> Optional[tuple[str, str]]:
        """Look up a user in the database."""

        user=get_user_by_name(username)
        if user is None:
            return None
        return (user.name, user.password_hash)

    result=login_flow(get_stored_user=lookup)

    if result is None:
        print("Login cancelled!")
        return None
    if not result.success:
        print("Login failed!")
        return None
    print(f"{result}")
    return result

def handle_dashboard() -> None:
    """Show the school dashboard."""
    show_dashboard()

# -------------------- Main loop --------------------
def main() -> None:
    """Run the top-level CLI loop."""
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT,datefmt=LOG_DATE_FORMAT)

    #Ensure the database is ready
    init_db()

    while True:
        print_menu()
        choice = ask_choice()
        if choice == "1":
            handle_registration()

        elif choice == "2":
            result = handle_login()
            if result and result.success:
                input("\nPress Enter to view the dashboard...")
                handle_dashboard()
                input("\nPress Enter to return to the menu...")

        elif choice == "3":
            print("\nGoodbye! 👋")
            break

        else:
            print("❌ Invalid option. Please choose 1, 2, or 3.")

# -------------------- Entry guard --------------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
    except Exception:
        logger.exception("Unexpected error")
        print("Something went wrong. Please try again.")
















































