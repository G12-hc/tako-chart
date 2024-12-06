import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import routers
from app.db.connection import initialize_db

# Create the API application instance
api_app = FastAPI(title="API app")
api_app.include_router(routers.router)

# Create the main application instance
app = FastAPI(title="main app")
app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    initialize_db()  # Initialize database or connections
    uvicorn.run(app, host="127.0.0.1", port=8000)

