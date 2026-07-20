from fastapi import FastAPI

tasks =[
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish report", "done": False},
    {"id": 3, "title": "Walk the dog", "done": True}
    ]
def get_current_id():   
    return len(tasks)
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
    
@app.post("/tasks/")
def post_task(title:str):
    if title and title.strip(" "):
        next_id = get_current_id() + 1
        done = False
        tasks.append({"id" : int(next_id) ,"title" : title, "done" : done})
        return {"Status"  : 201}
    return {"status" : 400}

@app.put("/tasks/:id")
def update_task(id: int, title : str, done : str):
    if title and title.strip(" ") and done and done.strip(" "):
        for task in tasks:
            if id == task.get("id"):
                task["title"] = title
                task["done"] = done 
                return {"status" : 204}
        return {"status" : 404}
    return {"status" : 400}
        
        

@app.get("/util/get_current_id")
def _get_current_id():
    return {"next id" : get_current_id()}


@app.get("/heath")
def get_health():
    return {"status" : "ok"}