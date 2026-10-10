"""
school_dashboard.py — Displays the school profile and user directory.

Responsibilities:
    - Hold static school information (name, motto, history, vision, mission)
    - Display the school profile
    - Fetch and display teachers from the database
    - Fetch and display students from the database

Public API:
    - show_dashboard() — displays everything
    - show_school_profile() — displays static info only
    - show_teachers() — displays teacher list from DB
    - show_students() — displays student list from DB

Note:
    This module does NOT handle authentication or flow control.
    The caller (main.py) is responsible for ensuring the user is logged in
    before calling show_dashboard().
"""
from  __future__ import annotations

import logging
from tools.sql_storage import User,list_users_by_role

logger = logging.getLogger(__name__)

# -------------------- Static school profile --------------------
SCHOOL_PROFILE: dict[str, str | list[str]] = {
    "name": "Minjila Comprehensive School",
    "motto": "Knowledge, Integrity, Service",
    "location": "Minjila, Tana River County, Kenya",
    "founded": "2017",
    "history": (
        "Minjila Comprehensive School was founded to provide quality education "
        "to the local community. Over the years it has grown into a center of "
        "academic excellence, serving hundreds of students from the region."
    ),
    "vision": (
        "To be a leading institution that nurtures holistic, creative, and "
        "responsible citizens ready to serve the nation and the world."
    ),
    "mission": (
        "To provide quality, inclusive education through innovation, discipline, "
        "and community partnership."
    ),
    "core_values": [
        "Integrity",
        "Discipline",
        "Excellence",
        "Respect",
        "Community Service",
    ],
}

# -------------------- Display helpers --------------------
def _print_header(title: str, width: int = 60) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def _print_divider(width: int = 60) -> None:
    print("-" * width)

# -------------------- Public display functions --------------------
def show_school_profile() -> None:
    """Display the static school profile."""
    _print_header("SCHOOL PROFILE")

    print(f"Name:      {SCHOOL_PROFILE['name']}")
    print(f"Motto:     {SCHOOL_PROFILE['motto']}")
    print(f"Location:  {SCHOOL_PROFILE['location']}")
    print(f"Founded:   {SCHOOL_PROFILE['founded']}")

    _print_divider()
    print("History:")
    print(f"  {SCHOOL_PROFILE['history']}")

    _print_divider()
    print("Vision:")
    print(f"  {SCHOOL_PROFILE['vision']}")

    _print_divider()
    print("Mission:")
    print(f"  {SCHOOL_PROFILE['mission']}")

    _print_divider()
    print("Core Values:")
    for value in SCHOOL_PROFILE["core_values"]:
        print(f"  • {value}")

    print("=" * 60)


def _display_user_table(users: list[User], title: str) -> None:
    """Print a list of users in a table-like format."""
    _print_header(title)

    if not users:
        print("  (no records)")
        print("=" * 60)
        return

    print(f"{'#':<4} {'Name':<25} {'Role':<15}")
    _print_divider()
    for i, user in enumerate(users, 1):
        print(f"{i:<4} {user.name:<25} {user.role:<15}")
    print("=" * 60)
    print(f"Total: {len(users)}")


def show_teachers() -> None:
    """Fetch and display all teachers."""
    teachers = list_users_by_role("teacher")
    _display_user_table(teachers, "TEACHERS")


def show_students() -> None:
    """Fetch and display all students."""
    students = list_users_by_role("student")
    _display_user_table(students, "STUDENTS")


def show_dashboard() -> None:
    """
    Display the complete school dashboard:
    profile + teachers + students.
    """
    logger.info("Displaying school dashboard")
    show_school_profile()
    show_teachers()
    show_students()


# -------------------- Demo --------------------
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    show_dashboard()

























































