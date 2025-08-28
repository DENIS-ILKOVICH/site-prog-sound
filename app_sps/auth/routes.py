from flask import *
from flask_login import *
from app_sps.auth.services.services import *
from app_sps.auth.src.login_form.login_form import LoginForm
from . import auth
from ..locales.load_language import load_language
from app_sps.logs.logclass import logger

@auth.route('/login', methods=['POST', 'GET'])
def login():
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        if current_user.is_authenticated:
            return redirect('/')

        form = LoginForm()
        if request.method == 'POST':
            response, status_code = auth_pr(db, form)
            if status_code == 422:
                return jsonify(response)
            return response

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu']

        return render_template('login.html', title='Sign in', form=form, menu=menu, content_ln=content_ln)
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@auth.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)
        response, status_code = logout_pr(current_user.get_id(), db)
        logout_status = response if status_code == 200 else None
        return logout_status
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@auth.route('/register', methods=['POST', 'GET'])
def register():
    try:
        logger.log_request(request)

        db = getattr(g, 'db', None)

        lang = session.get('language', 'en')
        content_ln = load_language(lang)

        menu = content_ln['menu']
        errors_list = content_ln['errors_list']

        response, status_code = register_pr(request, errors_list, db)
        if status_code == 400:
            flash_list = '\n'.join(response['error'])
            flash(flash_list, 'error')

        if status_code == 201:
            return redirect('/')

        return render_template('register.html', title='Register', menu=menu, content_ln=content_ln)
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise


@auth.route('/auto_login', methods=['POST', 'GET'])
def auto_login():
    try:
        logger.log_request(request)

        response, status_code = auto_login_pr()
        print(response, status_code)

        return response
    except Exception as e:
        logger.log_error("Internal Server Error", stack_trace=str(e))
    raise
