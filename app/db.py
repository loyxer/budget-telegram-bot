import sqlite3
from datetime import date, datetime, timedelta

from app.config import DB_PATH


def _connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = _connect()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            daily_count INTEGER NOT NULL DEFAULT 0,
            last_used_date TEXT,
            premium_until TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def _today():
    return date.today().isoformat()


def is_premium(user_id: int) -> bool:
    conn = _connect()
    row = conn.execute(
        "SELECT premium_until FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    if not row or not row[0]:
        return False
    return datetime.fromisoformat(row[0]) > datetime.now()


def remaining_free(user_id: int, limit: int) -> int:
    conn = _connect()
    row = conn.execute(
        "SELECT daily_count, last_used_date FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    if not row:
        return limit
    daily_count, last_used_date = row
    if last_used_date != _today():
        return limit
    return max(0, limit - daily_count)


def register_usage(user_id: int) -> None:
    today = _today()
    conn = _connect()
    row = conn.execute(
        "SELECT daily_count, last_used_date FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()

    if not row:
        conn.execute(
            "INSERT INTO users (user_id, daily_count, last_used_date) VALUES (?, 1, ?)",
            (user_id, today),
        )
    else:
        daily_count, last_used_date = row
        new_count = 1 if last_used_date != today else daily_count + 1
        conn.execute(
            "UPDATE users SET daily_count = ?, last_used_date = ? WHERE user_id = ?",
            (new_count, today, user_id),
        )
    conn.commit()
    conn.close()


def grant_premium(user_id: int, days: int) -> None:
    until = (datetime.now() + timedelta(days=days)).isoformat()
    conn = _connect()
    row = conn.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if row:
        conn.execute("UPDATE users SET premium_until = ? WHERE user_id = ?", (until, user_id))
    else:
        conn.execute(
            "INSERT INTO users (user_id, daily_count, last_used_date, premium_until) VALUES (?, 0, ?, ?)",
            (user_id, _today(), until),
        )
    conn.commit()
    conn.close()
