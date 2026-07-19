from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Custom exception handler for validation errors to return 400 and {"error": "..."}
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_msg = "Invalid body structure"
    if errors:
        loc = " -> ".join(str(l) for l in errors[0].get("loc", []))
        msg = errors[0].get("msg", "validation error")
        error_msg = f"Validation failed at {loc}: {msg}"
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": error_msg}
    )

# Task data model
class Task(BaseModel):
    id: int
    title: str
    done: bool

# Request model for creating a task
class TaskCreate(BaseModel):
    title: str

# Request model for updating a task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

# In-memory storage seeded with example tasks
tasks = [
    {"id": 1, "title": "Buy gold", "done": False},
    {"id": 2, "title": "Finish homework", "done": False},
    {"id": 3, "title": "Do laundry", "done": False}
]

@app.get("/tasks", response_model=list[Task], status_code=status.HTTP_200_OK)
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Task not found"}
    )

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    title = task_in.title.strip() if task_in.title else ""
    if not title:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Title is required and cannot be empty"}
        )
    
    new_id = max([t["id"] for t in tasks]) + 1 if tasks else 1
    new_task = {"id": new_id, "title": title, "done": False}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task_in: TaskUpdate):
    target_task = None
    for t in tasks:
        if t["id"] == task_id:
            target_task = t
            break
            
    if not target_task:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Task not found"}
        )
        
    if task_in.title is not None:
        title = task_in.title.strip()
        if not title:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Title cannot be empty"}
            )
        target_task["title"] = title
        
    if task_in.done is not None:
        target_task["done"] = task_in.done
        
    return target_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for idx, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(idx)
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Task not found"}
    )
