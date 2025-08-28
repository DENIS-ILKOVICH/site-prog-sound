from flask import g, session
from flask_login import LoginManager
from app_sps.auth.src.user_login.user_login import UserLogin
from app_sps.admin.src.admin_login.admin_login import AdminLogin
from app_sps.auth.models.models import Users
from app_sps.admin.models.admin_models.models import AdminModels

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login user loader callback.

    This function is used by Flask-Login to reload the user object from the user ID stored in the session.
    It supports both 'user' and 'admin' types based on the 'user_type' stored in the session.

    Args:
        user_id (str): The ID of the user to load.

    Returns:
        UserLogin | AdminLogin | None: Returns an instance of UserLogin or AdminLogin if the user is found,
        otherwise returns None.
    """
    db = getattr(g, 'db', None)

    user_type = session.get('user_type', None)
    if user_type and user_type == 'user':
        user_db = Users(db)
        user = user_db.getuser(user_id)
        if user:
            return UserLogin().fromDB(user_id, user_db)

    if user_type and user_type == 'admin':
        ad_db = AdminModels(db)
        admin = ad_db.get_admin_by_id(user_id)
        if admin:
            return AdminLogin().fromDB(user_id, ad_db)

    return None