import uvicorn
from fastapi import FastAPI

from app.routers import commits, branches, files, languages, repositories, licenses
from app.db.connection import initialize_db

# Create the FastAPI application instance

app = FastAPI()

app.include_router(commits.router)
app.include_router(branches.router)
app.include_router(files.router)
app.include_router(languages.router)
app.include_router(repositories.router)
app.include_router(licenses.router)



if __name__ == "__main__":
    initialize_db()  # Initialize database or connections
    uvicorn.run(app, host="127.0.0.1", port=8000)