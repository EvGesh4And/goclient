from flask import redirect, url_for


def group():
    return redirect(url_for("st0114.list_items"))
