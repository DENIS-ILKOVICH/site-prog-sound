from flask import *
from flask_login import *
from app_sps.auth.services.services import *
from app_sps.auth.src.login_form.login_form import LoginForm

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

from . import routes
from .database import database