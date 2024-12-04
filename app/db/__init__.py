# app/db/__init__.py

from .connection import get_db_connection

# Export the database connection utility
__all__ = ["get_db_connection"]
