from fastapi import FastAPI
from app.services import commits, repositories, branches, files, licenses, languages
from app.db.connection import initialize_db

# Create the FastAPI application instance
app = FastAPI()




# Initialize routers
def routers():
    app.include_router(commits.router, prefix="/commits", tags=["Commits"])
    app.include_router(files.router, prefix="/files", tags=["Files"])
    app.include_router(repositories.router, prefix="/repositories", tags=["Repositories"])
    app.include_router(branches.router, prefix="/branches", tags=["Branches"])
