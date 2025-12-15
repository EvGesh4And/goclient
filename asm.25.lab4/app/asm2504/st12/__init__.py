from flask import Blueprint
from .group import group

bp = Blueprint('st0412', __name__)


@bp.record_once
def _init_storage(state):
    from .db import init_db
    init_db()


from . import routes, api


@bp.route("/")
def main():
    return group().f()


@bp.route("/api/", methods=['GET'])
def api_main():
    return group().api()

