import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import routers
from app.db.connection import initialize_db

# Create the FastAPI application instance
app = FastAPI()
app.mount("/", StaticFiles(directory="frontend"), name="frontend")
app.include_router(routers.router)

if __name__ == "__main__":
    initialize_db()  # Initialize database or connections
    uvicorn.run(app, host="127.0.0.1", port=8000)