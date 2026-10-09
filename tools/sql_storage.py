"""
sql_storage.py — SQLite storage layer using SQLAlchemy 2.0 (modern).

Responsibilities:
    - Define the User model (single table for teachers and students)
    - Provide a session factory for the rest of the app
    - Expose CRUD functions: save_user, get_user_by_name, list_users_by_role

Public API:
    - init_db()
    - save_user(name, password_hash, role) -> User
    - get_user_by_name(name) -> User | None
    - list_users_by_role(role) -> list[User]
"""
from __future__ import annotations

from typing import Optional
import logging

from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import (
sessionmaker,
Session,
DeclarativeBase,
Mapped,
mapped_column
)

from config import DB_PATH
from tools.register import hash_password
from config import LOG_LEVEL, LOG_FORMAT, LOG_DATE_FORMAT


logger = logging.getLogger(__name__)

#---------------Model ------------------
class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass
class User(Base):
    """A user of the system — either a teacher or a student."""
    __tablename__ = "users"

    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column( String(100),unique=True,nullable=False)
    role:Mapped[str]=mapped_column( String(20),nullable=False)
    password_hash:Mapped[str]=mapped_column( String(255),nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r}, role={self.role!r})"

# -------------------- Engine & Session --------------------
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def init_db() -> None:
    """Create tables if they don't exist. Safe to call multiple times."""
    Base.metadata.create_all(engine)
    logger.info("Database initialized at %s", DB_PATH)
# -------------------- CRUD --------------------

def save_user(name: str, password_hash: str, role: str) -> User:
    """
     Insert a new user. Raises ValueError if the name already exists.
     """
    with SessionLocal() as session:
        #check if exists
        existing=session.scalar(select(User).where(User.name==name))
        if existing is not None:
            raise ValueError(f"User with name {name!r} already exists")
        user = User(name=name, password_hash=password_hash, role=role)
        session.add(user)
        session.commit()
        session.refresh(user)
        logger.info("Saved user %r",user)
        return user

def get_user_by_name(name: str) -> Optional[User]:
    """Fetch a single user by name, or None."""
    with SessionLocal() as session:
        return session.scalar(select(User).where(User.name==name))


def list_users_by_role(role: str) -> list[User]:
    """Return all users with the given role."""
    with SessionLocal() as session:
        stmt=select(User).where(User.role==role).order_by(User.name)
        return list(session.scalars(stmt))


# -------------------- Demo --------------------
if __name__=="__main__":
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
    )
    init_db()

    #add user samples
    for name,pw,role in[
        ( "Nadibho","nadibho_ywetoo124","teacher"),
            ( "Babuura","baabura_mokolo12","student")
        ]:
        try:
            save_user(name,hash_password(pw),role)
        except ValueError as e:
            print(f"ValueError: {e}")

    #fetch one
    get_dadibho=get_user_by_name("Nadibho")
    print(get_dadibho)
    #list by roles
    print("\nTeachers")
    for t in list_users_by_role("teacher"):
        print(t)

    print("\nStudents")
    for s in list_users_by_role("student"):
        print(s)
















































































