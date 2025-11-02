from fastapi import FastAPI

app = FastAPI(title="Authentication Backend")

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI authentication backend is running!"}
