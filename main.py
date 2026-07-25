from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from database import get_connection, initialize_database

app = FastAPI()

initialize_database()

tasks = []
class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


@app.get("/")
async def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/tasks")
async def get_tasks():
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("""
                SELECT id, title, done
                FROM tasks
                ORDER BY id
            """)
            rows = cur.fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }
        for row in rows
    ]


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("""
                SELECT id, title, done
                FROM tasks
                WHERE id = %s
            """, (task_id,))

            row = cur.fetchone()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }


@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )

    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("""
                INSERT INTO tasks (title, done)
                VALUES (%s, %s)
                RETURNING id, title, done
            """, (task.title, False))

            row = cur.fetchone()

        con.commit()

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: TaskUpdate):
    if task.title is None or not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )

    if task.done is None:
        task.done = False

    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("""
                UPDATE tasks
                SET title = %s,
                    done = %s
                WHERE id = %s
                RETURNING id, title, done
            """, (task.title, task.done, task_id))

            row = cur.fetchone()

        con.commit()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("""
                DELETE FROM tasks
                WHERE id = %s
                RETURNING id
            """, (task_id,))

            row = cur.fetchone()

        con.commit()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return Response(status_code=204)