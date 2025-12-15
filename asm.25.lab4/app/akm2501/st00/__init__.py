from flask import Blueprint

# Изменить на свой код

bp = Blueprint('st0100', __name__)

from .group import group

@bp.route("/")
def main():
	return group().f()

@bp.route("/api/", methods=['GET'])
def api():
	return group().api()
