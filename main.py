from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from fastapi import *

app = FastAPI() 


tasks = [  
     { "id" : 1, "title" : "Buy gold", "completed" : False}, 
     { "id" : 2, "title" : "Finish homework", "completed" : False} , 
     { "id" : 3, "title" : "Do laundry", "completed" : False}  ]

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

    



                
    
            
            



                
    
