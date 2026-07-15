from fastapi import FastAPI

tasks =[
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish report", "done": False},
    {"id": 3, "title": "Walk the dog", "done": True}
    ]
app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Hello World"}

@app.get("/tasks")
def get_tasks():
    return {"tasks" : tasks}

@app.get("/tasks/{id}")
def get_task_by_id(id:int):
    for task in tasks:
        if task.get("id") == id:
            return {"task" : task for task in tasks if task.get("id") == id }
    return {"status" : 404,
            "error" : f"Task {id} not found."}

@app.get("/heath")
def get_health():
    return {"status" : "ok"}