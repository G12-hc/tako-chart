from fastapi import FastAPI
from app.services import commits, repositories, branches, files, licenses, languages
from app.db.connection import initialize_db

# Create the FastAPI application instance
app = FastAPI()




# Initialize services (placeholder, as services are directly imported in routers)
def services():
    pass


# Initialize database (if any one-time setup is required)
def db():
    initialize_db()


# Application startup
def create_app():
    routers()  # Attach all routers
    db()  # Initialize database or connections
    return app
