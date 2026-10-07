import sqlite3


def get_connection():
    return sqlite3.connect("assistant.db")


def init_db():

    connection = get_connection()

    cursor = connection.cursor()

    # =========================
    # TASKS TABLE
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    # =========================
    # EXPENSES TABLE
    # =========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    # =========================
    # STUDY TABLE
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        topic TEXT NOT NULL,
        duration INTEGER NOT NULL,
        date TEXT NOT NULL
    )
""")

    # =========================
    # GROCERY TABLE
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groceries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        quantity TEXT,
        bought INTEGER DEFAULT 0
    )
""")

    # =========================
    # NOTES TABLE
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        date TEXT NOT NULL
    )
""")

    # =========================
    # REMINDERS TABLE
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        reminder_time TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
""")

    # =========================
    # GOALS TABLE
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        target_date TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
""")

    connection.commit()
    connection.close()