# app_spt/database.py
from flask import g
import sqlite3
from config import Config


class Database:
    def __init__(self):
        """
        Initialize a database connection object for the application.

        Attributes:
            database_location (str): Path to the SQLite database file.
            db (sqlite3.Connection or None): Database connection object.
        """
        self.database_location = Config.DATABASE
        self.db = None

    def get_db(self):
        """
        Retrieve or create a SQLite database connection for the current Flask request context.

        If a connection already exists in `g`, it will be reused. Otherwise, a new connection
        is created and stored in `g`. Row factory is set to sqlite3.Row for dict-like access.

        Returns:
            sqlite3.Connection: Database connection object, or None if connection failed.
        """
        if 'db' not in g:
            try:
                g.db = sqlite3.connect(self.database_location)
                g.db.row_factory = sqlite3.Row
            except sqlite3.Error as e:
                g.db = None
        return g.db

    @staticmethod
    def close():
        """
        Close the SQLite database connection stored in Flask `g`.

        Should be called after the request finishes to release the database resources.
        """
        db = getattr(g, 'db', None)
        if db is not None:
            db.close()


db_instance = Database()