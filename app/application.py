from fastapi import FastAPI

from app.routers import get_all_repo_data
from app.db.connection import initialize_db

def get_app() -> FastAPI:
    initialize_db()
    app = FastAPI()
    app.include_router(get_all_repo_data.router)

    return app
