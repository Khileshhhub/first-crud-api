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
    completed: Optional[bool] = None


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

    for task in tasks:

        if task["id"] == id:

            if updated_task.title is not None:

                if updated_task.title.strip() == "":
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title cannot be empty"}
                    )

                task["title"] = updated_task.title.strip()

            if updated_task.done is not None:
                task["done"] = updated_task.done

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )


@app.delete("/tasks/{id}", status_code=204)
async def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

    



                
    
            
            



                
    
