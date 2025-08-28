from flask_login import *
from app_sps.playlist.services.services import *
import io
from flask import *

playlist = Blueprint('playlist', __name__, template_folder='templates', static_folder='static')

from . import routes
# from app_sps.playlist.database.database import *
from .database import database
