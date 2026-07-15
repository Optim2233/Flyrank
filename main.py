from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Hello World"}

@app.get("/tasks")
def get_tasks():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/heath")
def get_health():
    return {"status" : "ok"}