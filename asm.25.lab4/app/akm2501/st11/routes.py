from flask import render_template, request, redirect, url_for

from . import bp
from .pet_shop import PetShop
from .io_strategy import FlaskIOStrategy
from .storage import SQLiteStorage
from .models import Animal, Predator, Herbivore
from .group import group


def _author_name():
    raw = group().f()
    if "(" in raw and raw.endswith(")"):
        return raw.split("(", 1)[1][:-1]
    return raw


AUTHOR = _author_name()
TITLE = "Картотека животных"

TYPE_MAP = {
    Animal.__name__: Animal,
    Predator.__name__: Predator,
    Herbivore.__name__: Herbivore,
}

shop = PetShop(FlaskIOStrategy(), SQLiteStorage(type_resolver=lambda n: TYPE_MAP.get(n)))


@bp.route("/")
def index():
    animals = shop.show_catalog()
    return render_template(
        "akm2501/st11/index.html",
        title=TITLE,
        author=AUTHOR,
        animals=animals,
    )


@bp.route("/create_animal", methods=["GET", "POST"])
def create_animal():
    if request.method == "POST":
        shop.add_animal()
        return redirect(url_for("st0111.show_animals"))

    return render_template(
        "akm2501/st11/create_animal.html",
        title=TITLE,
        author=AUTHOR,
    )


@bp.route("/show_animals")
def show_animals():
    animals = shop.show_catalog()
    return render_template(
        "akm2501/st11/animals_list.html",
        animals=animals,
        title=TITLE,
        author=AUTHOR,
    )


@bp.route("/edit_animal/<string:animal_id>", methods=["GET", "POST"])
def edit_animal(animal_id):
    animal = shop.get_by_id(animal_id)
    if not animal:
        return redirect(url_for("st0111.show_animals"))

    if request.method == "POST":
        shop.edit_animal(animal_id)
        return redirect(url_for("st0111.show_animals"))

    return render_template(
        "akm2501/st11/edit_animal.html",
        animal=animal,
        title=TITLE,
        author=AUTHOR,
    )


@bp.route("/delete_animal/<string:animal_id>")
def delete_animal(animal_id):
    shop.delete_animal(animal_id)
    return redirect(url_for("st0111.show_animals"))


@bp.route("/dump")
def dump():
    shop.save()
    return redirect(url_for("st0111.show_animals"))


@bp.route("/load")
def load():
    shop.load()
    return redirect(url_for("st0111.show_animals"))


@bp.route("/clear")
def clear():
    shop.clear_catalog()
    return redirect(url_for("st0111.show_animals"))

