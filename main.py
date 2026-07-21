from fastapi import FastAPI
from typing import Optional
import re
import sqlite3


tasks =[
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish report", "done": False},
    {"id": 3, "title": "Walk the dog", "done": True}
    ]

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS tasks(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   done BOOLEAN NOT NULL
                   )
                   """)
count = cursor.execute("SELECT COUNT(*) FROM tasks")
if count == 0:
    cursor.executemany("INSERT INTO tasks VALUES(:id,:title,:done)", tasks)

conn.commit()

for row in cursor.execute("SELECT title, done FROM tasks"):
    print(row)



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
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    query = "SELECT * FROM tasks WHERE id = ?"
    params = [id]
    cursor.execute(query,params)
    rows = cursor.fetchone()
    conn.close()
    if rows:
        return {"id": rows[0], "title": rows[1], "done" : rows[2]}
    return {"status" : 404,
            "error" : f"Task {id} not found."}
    

@app.get("/tasks", tags=["get tasks"])
def get_done_task(search_term : str = " " ,done: Optional[bool] = None):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    query = "SELECT * FROM tasks WHERE 1=1"
    parameter = []
    if search_term.strip():
        query += " AND title LIKE ?" 
        parameter.append(f"%{search_term.strip()}%")
    if done is not None:
        query += " AND done = ?"
        parameter.append(done)
        
    cursor.execute(query,parameter) 
    rows = cursor.fetchall()
    conn.close()
    tasks = [{"id" : r[0], "title": r[1], "done": bool(r[2])} for r in rows]
    
    return {"tasks" : tasks}
    
@app.post("/tasks/post_tasks", tags=["create task"])
def post_task(title:str):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    id = get_current_id()
    
    if title and title.strip(" "):
        next_id = get_current_id() + 1
        query = f"INSERT INTO tasks VALUES(:id,:title,:done)"
        new_task = {"id" : next_id, "title" : title, "done" : bool(False)}
        cursor.execute(query,new_task)
        conn.commit()
        return {"Status"  : 201}
    return {"status" : 400}

@app.put("/tasks/{id}", tags=["update task"])
def update_task(id: int, title : str, done : bool):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    query = "UPDATE tasks SET title = ? , done = ? WHERE id = ?"
    params = [title,done,id]
    cursor.execute(query,params)
    if cursor.rowcount == 0:
        conn.close()
        return {"status " : 404}
    elif cursor.rowcount >= 1:
        conn.commit()
        return {"status" : 204}
    conn.close()
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
    
@app.delete("/tasks/delete_tasks", tags=["delete tasks"])
def delete_tasks(id : int ):
    conn = sqlite3.connect("tasks.db")  
    cursor = conn.cursor()
    query = "DELETE FROM tasks WHERE id = ?"
    params = [id]
    cursor.execute(query,params)
    if cursor.rowcount == 0:
        return {"status" : 404}
    conn.commit()
    conn.close() 
    return {"status" : 204}
    
    
    
    