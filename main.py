from fastapi import FastAPI
from typing import Optional
import re
tasks =[
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish report", "done": False},
    {"id": 3, "title": "Walk the dog", "done": True}
    ]

tags_metadata = [
    {
        "name"  : "get tasks",
        "description" : "Get the existing tasks"
    },
    {
        "name" : "get task by id",
        "description": "Get task by id from existing tasks"
    },
    {
        "name" : "create task",
        "description":"create task "
    },
    {
        "name" : "update task",
        "description" : "update existing task"
    },
    {
        "name" : "get the pointer location of current id",
        "description" : "helper fucntion made api end point"
    },
    {
        "name": "health",
        "description" :"health check"
    },
    {
        "name" : "get stats",
        "description" : "get statisics of tasks"
    }
]

def get_current_id():   
    return len(tasks)
app = FastAPI(openapi_tags=tags_metadata)

@app.get("/")
def root():
    return {"message" : "Hello World"}

@app.get("/tasks/{id}",tags=["get task by id"])
def get_task_by_id(id:int):
    for task in tasks:
        if task.get("id") == id:
            return {"task" : task for task in tasks if task.get("id") == id }
    return {"status" : 404,
            "error" : f"Task {id} not found."}
    

@app.get("/tasks", tags=["get tasks"])
def get_done_task(search_term : str = " " ,done: Optional[bool] = None):
    if done == None and not search_term.strip(" "):
        return {"tasks" : tasks}
    elif done == None and search_term.strip(" "):
        filtered = [task for task in tasks  if re.search(re.escape(search_term), task["title"], re.IGNORECASE)]
    elif done != None and not search_term.strip(" "):
        filtered = [task for task in tasks if task.get("done") == done]
    else : 
        filtered = [ task for task in tasks if task.get("done") == done and re.search(re.escape(search_term), task["title"], re.IGNORECASE) ]
    
    return {"tasks" : filtered}
    
@app.post("/tasks/", tags=["create task"])
def post_task(title:str):
    if title and title.strip(" "):
        next_id = get_current_id() + 1
        done = False
        tasks.append({"id" : int(next_id) ,"title" : title, "done" : done})
        return {"Status"  : 201}
    return {"status" : 400}

@app.put("/tasks/{id}", tags=["update task"])
def update_task(id: int, title : str, done : bool):
    if title and title.strip(" ") and done != None:
        for task in tasks:
            if task.get("id") == id:
                task["title"] = title
                task["done"] = done 
                return {"status" : 204}
        return {"status" : 404}
    return {"status" : 400}
        

@app.get("/util/get_current_id", tags=["get the pointer location of current id"])
def _get_current_id():
    return {"next id" : get_current_id()}


@app.get("/heath", tags=["health"])
def get_health():
    return {"status" : "ok"}

@app.get("/stats", tags=["get stats"])
def get_stats( ):
    done_tasks = []
    open_tasks = []
    for task in tasks:
        if task.get("done") == True:
            done_tasks.append(task)
        else : 
            open_tasks.append(task)
    return {
        "total" : len(tasks),
        "done" : len(done_tasks),
        "open" : len(open_tasks)}