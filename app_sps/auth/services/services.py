# app_sps/auth/services/services.py
from app_sps.auth.models.models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from app_sps.auth.src.user_login.user_login import UserLogin
from flask import *
from flask_login import *
from datetime import *
from app_sps.auth.src.utils.utils import Utils
from app_sps.locales.load_language import load_language
from app_sps.logs.logclass import logger
from database import db_instance

utils = Utils()

def auth_pr(db, form):
    """
    Authenticate a user using form data.

    Args:
        db: Database connection.
        form: Flask-WTF form with fields 'mail', 'psw', and 'remember_me'.

    Returns:
        tuple or dict: JSON response with success status, messages, and optional redirect URL.
        Sets session data and remember_token cookie if requested.
    """
    try:
        userdb = Users(db)

        lang = session.get('language', 'en')
        messages = load_language(lang)['login']['messages']

        if not form.validate_on_submit():
            return {'success': False, 'message': messages[0], 'category': 'warning'}, 422

        user = userdb.get_user_by_email(form.mail.data)
        if not user:
            return {'success': False, 'message': messages[1], 'category': 'info'}, 422

        pass_db = user['password']
        pass_form = form.psw.data
        if not check_password_hash(pass_db, pass_form):
            return {'success': False, 'message': messages[2], 'category': 'error'}, 422

        user_login = UserLogin().create(user)
        if not user_login:
            return {}

        session['user_type'] = 'user'
        login_user(user_login)
        session['user_id'] = current_user.get_id()

        if form.remember_me.data:
            token = userdb.generate_remember_token(current_app.secret_key, current_user.get_id())

            response = make_response(
                jsonify({'success': True, 'redirect': request.args.get("next") or url_for('content.index')}))

            expires = datetime.now() + timedelta(days=30)

            response.set_cookie('remember_token', token, expires=expires, httponly=True)

            return response, 200

        return {'success': True, 'redirect': request.args.get("next") or url_for('content.index')}, 200

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500



def logout_pr(user_id, db):
    """
    Log out the currently authenticated user.

    Args:
        user_id: ID of the user to clear the remember token.
        db: Database connection.

    Returns:
        tuple: Flask response object for redirect and HTTP status code.
        Deletes remember_token cookie and logs out the user.
    """
    try:
        user = Users(db)

        if current_user.is_authenticated:
            user.remember_token_none(user_id)

        response = make_response(redirect(url_for('auth.login')))
        response.delete_cookie('remember_token')
        logout_user()

        return response, 200

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def register_pr(req, errors_list,  db):
    """
    Register a new user using form data from the request.

    Args:
        req: Flask request object with form fields 'name', 'mail', 'psw', and 'psw2'.
        errors_list: List to collect validation errors.
        db: Database connection.

    Returns:
        dict: JSON response with registration success or error details.
        Automatically logs in the newly registered user and sets session data.
    """
    try:
        if not req:
            return {'error': 'Invalid input'}, 400

        user = Users(db)

        name = request.form.get('name', '').strip()
        email = request.form.get('mail', '').strip()
        psw = request.form.get('psw', '').strip()
        psw2 = request.form.get('psw2', '').strip()

        if not all([name, email, psw, psw2]):
            raise ValueError('Invalid data input')

        result = utils.validate_registration(name, email, psw, psw2, errors_list)
        if not result["success"]:
            return {'error': result['errors']}, 400

        hash_psw = generate_password_hash(psw)
        user_id = user.adduser(name, email, hash_psw)
        if not user_id:
            raise ValueError('Invalid data input')

        userlogin = UserLogin().create(user_id)
        login_user(userlogin)
        session['user_id'] = current_user.get_id()

        return {'success': True}, 201

    except ValueError as e:
        return {'error': 'Invalid input', 'details': str(e)}, 422

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


def auto_login_pr():
    """
    Automatically log in a user using the 'remember_token' cookie.

    Returns:
        dict: JSON response with authorization status and messages.
        Sets session data and logs in the user if the token is valid.
    """
    try:
        db = db_instance.get_db()

        userdb = Users(db)
        response = {}

        if current_user.is_authenticated:
            return {'status': 'failed', 'error': 'Already logged in'}, 403

        remember_token = request.cookies.get('remember_token')
        if not remember_token:
            return {'status': 'failed', 'error': 'Invalid user id data'}, 400

        user = userdb.verify_remember_token(remember_token, current_app.secret_key)
        if not user:
            return {'status': 'failed', 'error': 'Invalid input data in cookies'}, 400

        userlogin = UserLogin().create(user)

        session['user_type'] = 'user'
        login_user(userlogin)
        session['user_id'] = current_user.get_id()

        return {'status': 'success', 'message': 'Successful authorization'}, 200

    except Exception as e:
        logger.log_error("Internal server error in services", stack_trace=str(e))
        return {'error': 'An unexpected error occurred'}, 500


