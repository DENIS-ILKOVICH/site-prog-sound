from database import db_instance
from app_sps.auth import auth


@auth.before_request
def before_request():
    db_instance.get_db()



@auth.teardown_request
def close_db(error=None):
    db_instance.close()
