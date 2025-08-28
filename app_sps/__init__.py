# app_sps/__init__.py
from flask import Flask, render_template
from werkzeug.exceptions import HTTPException
from app_sps.logs.logclass import logger, logging
from config import Config
from app_sps.extensions import login_manager
from app_sps.content.src.cache.cache import Cache


def create_app():
    """Create and configure a Flask application instance, load configuration and route
    authorization, content and playlist workflows"""
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Авторизуйтесь для дальнейшего пользования сайтом"
    login_manager.login_message_category = 'success'

    from app_sps.auth.routes import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from app_sps.content.routes import content
    app.register_blueprint(content, url_prefix="/")

    from app_sps.playlist.routes import playlist
    app.register_blueprint(playlist, url_prefix="/playlist")

    from app_sps.admin.routes import admin
    app.register_blueprint(admin, url_prefix="/admin")

    with app.app_context():
        app.cache = Cache()
        app.cache.load_search_data()

    return app
