from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="Simple Calculator API",
    description="A simple calculator FastAPI application with various math operations.",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Simple Calculator API. Go to /docs for more info."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
