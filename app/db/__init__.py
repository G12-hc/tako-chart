# app/db/__init__.py

from .connection import db_connection

# Export the database connection utility
__all__ = ["db_connection"]
