from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix="/api/v1")

from . import api_view
from . import address_view
from . import cart_view