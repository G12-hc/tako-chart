import uvicorn
from fastapi import FastAPI

from app import routers, git_router
from app.db.connection import initialize_db

# Create the FastAPI application instance
app = FastAPI()
app.include_router(routers.router)
app.include_router(git_router.router)
app.include_router(routers.tmp_router)


if __name__ == "__main__":
    initialize_db()  # Initialize database or connections
    uvicorn.run(app, host="127.0.0.1", port=8000)
