from flask import Blueprint, Flask

bp = Blueprint('bp', __name__,
                 template_folder='../../templates/asm2504/st23',
                 static_folder='../../static/asm2504/st23')

from .routes import bp
from .api import bp