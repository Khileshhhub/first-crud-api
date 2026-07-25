from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from fastapi import *
from database import initialize_db
from database import get_connection
from fastapi import HTTPException

app = FastAPI()

initialize_db()

tasks = [
]

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
        "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return JSONResponse({"status" : "ok"})

@app.get("/tasks")
async def get_tasks():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()

    cur.close
    return [dict(row) for row in rows]

@app.get("/tasks/{id}")
async def get_task(id: int):
    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM tasks WHERE id=?",(id,)
    )
    row = cur.fetchone()
    con.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "Task not found"}
        )

    return dict(row)

@app.post("/tasks")
async def create_task(task: TaskCreate):
    title = task.title.strip()
    
    if not title :
        return JSONResponse(content={"error" : "Title is required"}, status_code = 400)

    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO tasks (title, done) VALUES (?,?)", (title, False)
    )
    con.commit()
    new_id = cur.lastrowid
    con.close()

    return {
        "id": new_id,
        "title": title,
        "done": False
    }



@app.put("/tasks/{id}")
def update_task(id: int, updated_task: TaskUpdate):

    if not updated_task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )

    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "UPDATE tasks SET title=?, done = ? WHERE id = ?",
        (updated_task.title, updated_task.done, id)
    )

    con.commit()
    if cur.rowcount == 0:
        con.close()
        raise HTTPException(
            status_code=404, 
            detail={"error" : "Task not found"}
        )
    
    cur.execute(
        "SELECT * FROM tasks WHERE id=?",(id,)
    )
    updated_task = dict(cur.fetchone())
    con.close()

    return updated_task



@app.delete("/tasks/{id}", status_code=204)
async def delete_task(id: int):

    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id=?",(id,)
    )

    con.commit()

    if cur.rowcount == 0:
        con.close()
        raise HTTPException(
            status_code=404, 
            detail={"error" : "Task not found"}
        )

    con.close()
    return Response(status_code=204)

    



                
    
            
            



                
    
