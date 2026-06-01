from fastapi import FastAPI

app = FastAPI()

VERSION = "0.0.1"
@app.get("/health")
def health():
    return {"status": "UP"}

@app.get("/version")
def get_version():
    return {"version": VERSION}