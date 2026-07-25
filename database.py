import sqlite3

DB_name = "tasks.db"

def get_connection():
    con = sqlite3.connect(DB_name)
    con.row_factory = sqlite3.Row
    return con

def initialize_db():
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL
    )
    """)

    cur.execute("""
    SELECT COUNT(*) FROM tasks
    """)
    count = cur.fetchone()[0]

    if count == 0:
        cur.executemany(
        "INSERT INTO tasks (title, done) VALUES (?,?) ",
        [
        ("Buy gold", False),
        ("Finish homework", False),
        ("Do laundry", False)
        ],
        )
    con.commit()
    con.close()
