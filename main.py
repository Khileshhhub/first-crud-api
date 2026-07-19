from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI() 

tasks = [  
     { "id" : 1, "title" : "GET", "completed" : False}, 
     { "id" : 2, "title" : "POST", "completed" : False} , 
     { "id" : 3, "title" : "PUT", "completed" : False} , 
     { "id" : 4, "title" : "DELETE", "completed" : False}  ]
class TaskCreate(BaseModel):
    title: str

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
    return tasks

@app.get("/tasks/{id}")
async def get_task(id: int):

    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse({"error" : f"Task {id} not found"}, status_code = 404)

@app.post("/tasks")
async def create_task(task: TaskCreate):
    title = task.title.strip()
    
    if not title :
        return JSONResponse(content={"error" : "Title is required"}, status_code = 400)
    
    next_id = (max([task["id"] for task in tasks] + [0])) + 1
    new_task = {
        "id": next_id,
        "title": title,
        "completed":False
    }
    tasks.append(new_task)
    return new_task