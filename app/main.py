
from fastapi import FastAPI
import uvicorn
from app.routers import commits, repositories, branches, files, licenses, languages

app = FastAPI()

# Include routes
app.include_router(commits.router, prefix="/commits", tags=["Commits"])
app.include_router(repositories.router, prefix="/repositories", tags=["Repositories"])
app.include_router(branches.router, prefix="/branches", tags=["Branches"])
app.include_router(files.router, prefix="/files", tags=["Files"])
app.include_router(licenses.router, prefix="/licenses", tags=["Licenses"])
app.include_router(languages.router, prefix="/languages", tags=["Languages"])

###


from app import create_app

app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)