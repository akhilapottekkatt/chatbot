import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chatbot.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Columns added after initial deploy; SQLite does not auto-migrate on create_all().
_SQLITE_COLUMN_MIGRATIONS = {
    "messages": [
        ("user_id", "TEXT NOT NULL DEFAULT 'default'"),
        ("crisis_flag", "INTEGER NOT NULL DEFAULT 0"),
    ],
    "moods": [
        ("user_id", "TEXT NOT NULL DEFAULT 'default'"),
        ("note", "TEXT"),
    ],
    "journal_entries": [
        ("user_id", "TEXT NOT NULL DEFAULT 'default'"),
    ],
    "goals": [
        ("user_id", "TEXT NOT NULL DEFAULT 'default'"),
        ("progress_note", "TEXT"),
    ],
}


def run_sqlite_migrations(eng) -> None:
    """Add missing columns on SQLite when the DB file predates model changes."""
    if not str(eng.url).startswith("sqlite"):
        return
    with eng.begin() as conn:
        for table, columns in _SQLITE_COLUMN_MIGRATIONS.items():
            exists = conn.execute(
                text("SELECT 1 FROM sqlite_master WHERE type='table' AND name=:t"),
                {"t": table},
            ).scalar()
            if not exists:
                continue
            rows = conn.execute(text(f"PRAGMA table_info({table})")).fetchall()
            existing = {row[1] for row in rows}
            for col_name, col_def in columns:
                if col_name in existing:
                    continue
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_def}"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()