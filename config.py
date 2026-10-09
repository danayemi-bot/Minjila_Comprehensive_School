"""
config.py — Central configuration for the Minjila Comprehensive School project.

Every module imports its settings from here. Change a value once, and
the whole project picks it up.
"""

from pathlib import Path

# -------------------- Paths --------------------
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "school.db"
LOG_PATH = BASE_DIR / "school.log"

# -------------------- Application --------------------
APP_NAME = "Minjila Comprehensive School"
APP_VERSION = "0.1.0"

# -------------------- Security / Auth --------------------
PASSWORD_MIN_LEN = 8
PASSWORD_MAX_LEN = 64
MAX_LOGIN_ATTEMPTS = 5
VALID_ROLES = {"teacher", "student"}
PASSWORD_SALT = "static_salt_change_me"   #

# -------------------- Logging --------------------
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"