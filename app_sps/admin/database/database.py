from database import db_instance
from app_sps.admin import admin


@admin.before_request
def before_request():
    """Handler that runs before each request to establish a database connection."""
    db_instance.get_db()  # Initialize a database connection using the DB class


@admin.teardown_request
def close_db(error=None):
    """Handler that runs after each request to close the database connection."""
    db_instance.close()  # Close the database connection using the DB class



