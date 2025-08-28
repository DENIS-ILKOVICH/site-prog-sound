from database import db_instance
from app_sps.playlist import playlist


@playlist.before_request
def before_request():
    db_instance.get_db()


@playlist.teardown_request
def close_db(error=None):
    db_instance.close()
