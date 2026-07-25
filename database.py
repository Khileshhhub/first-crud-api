import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def initialize_database():
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)

            cur.execute("SELECT COUNT(*) FROM tasks")
            count = cur.fetchone()[0]

            if count == 0:
                cur.executemany(
                    """
                    INSERT INTO tasks (title, done)
                    VALUES (%s, %s)
                    """,
                    [
                        ("Buy groceries", False),
                        ("Finish homework", False),
                        ("Do laundry", False),
                    ],
                )

        con.commit()