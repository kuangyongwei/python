from flask import Blueprint

cms_bp = Blueprint('cms', __name__, url_prefix='/cms')

from apps.cms import cms_view
from apps.cms import shop_view
from apps.cms import food_view
