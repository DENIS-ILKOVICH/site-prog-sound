from database import db_instance
from app_sps.content import content


@content.before_request
def before_request():
    db_instance.get_db()

@content.teardown_request
def close_db(error=None):
    db_instance.close()
