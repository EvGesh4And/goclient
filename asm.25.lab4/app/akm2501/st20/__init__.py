from flask import Blueprint

bp = Blueprint('st0120', __name__, template_folder='templates/akm2501/st20')
from . import routes