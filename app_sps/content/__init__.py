from flask import *
from app_sps.content.services.services import *
from app_sps.content.src.cache.cache import Cache

content = Blueprint('content', __name__, template_folder='templates', static_folder='static')

from . import routes
from .database import database