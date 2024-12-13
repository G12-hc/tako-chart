import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import routers
from app.db.connection import open_connection_pool, close_connection_pool


def create_app():
    # Create the API application instance
    api_app = FastAPI(title="API app")
    api_app.include_router(routers.router)

    # Create the main application instance
    app = FastAPI(title="main app")
    app.mount("/api", api_app)
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

    @app.on_event("startup")
    async def startup():
        print("Opening connection pool...")
        await open_connection_pool()

    @app.on_event("shutdown")
    async def shutdown():
        print("Closing connection pool...")
        await close_connection_pool()

    return app


if __name__ == "__main__":
    uvicorn.run("app.main:create_app", host="127.0.0.1", port=8000, reload=True)
