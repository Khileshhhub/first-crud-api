from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI() 

tasks = [  
     { "id" : 1, "title" : "GET", "completed" : False}, 
     { "id" : 2, "title" : "POST", "completed" : False} , 
     { "id" : 3, "title" : "PUT", "completed" : False} , 
     { "id" : 4, "title" : "DELETE", "completed" : False}  ]

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


