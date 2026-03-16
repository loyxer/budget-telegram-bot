import sqlite3

conn = sqlite3.connect("budget.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS budgets (
    chat_id INTEGER PRIMARY KEY,
    start_budget INTEGER,
    spent INTEGER,
    start_date TEXT
)
""")

conn.commit()


def set_budget(chat_id, start_budget, start_date):
    cursor.execute(
        "INSERT OR REPLACE INTO budgets VALUES (?, ?, ?, ?)",
        (chat_id, start_budget, 0, start_date)
    )
    conn.commit()


def add_expense(chat_id, amount):
    cursor.execute(
        "UPDATE budgets SET spent = spent + ? WHERE chat_id = ?",
        (amount, chat_id)
    )
    conn.commit()


def get_budget(chat_id):
    cursor.execute(
        "SELECT start_budget, spent, start_date FROM budgets WHERE chat_id = ?",
        (chat_id,)
    )
    return cursor.fetchone()