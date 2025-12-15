from flask import Blueprint

bp = Blueprint('group', __name__)

from . import roots
