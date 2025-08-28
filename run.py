# run.py
from app_sps import create_app
from werkzeug.exceptions import HTTPException
from flask import session, render_template, g
from app_sps.auth.routes import auto_login
from app_sps.content.routes import language
from app_sps.logs.logclass import logger
from app_sps.locales.load_language import load_language

sound = create_app()

@sound.before_request
def before_request():
    """
    Execute pre-request actions before handling each request in the 'sound' Blueprint.

    This function ensures that on the first request:
        - The user is automatically logged in via `auto_login()`.
        - The language is initialized via `language()`.

    It sets a session flag 'first_request_done' to avoid repeating these actions.
    """
    if "first_request_done" not in session:
        session["first_request_done"] = True
        auto_login()
        language()

@sound.errorhandler(Exception)
def handle_exception(e):
    """
    Handle all uncaught exceptions within the 'sound' Blueprint.

    Logs the error, determines the HTTP status code and language-specific content,
    and renders the error page with appropriate context.

    Args:
        e (Exception): The exception instance raised during request handling.

    Returns:
        Response: Flask rendered template response for 'error.html' with status code.
    """
    code = 500
    description = "Internal Server Error"
    db = getattr(g, 'db', None)
    lang = session.get('language', 'en')
    content_ln = load_language(lang)
    menu = content_ln['menu']
    if isinstance(e, HTTPException):
        logger.log_error("Internal Server Error", stack_trace=f'{e.description}, {e.code}')

    return render_template("error.html", title='Error', code=code, description=description, content_ln=content_ln, menu=menu), code

if __name__ == '__main__':
    sound.run(debug=True)
