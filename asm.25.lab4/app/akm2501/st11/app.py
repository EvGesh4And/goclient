from flask import Flask, render_template, request, redirect, url_for, flash
import sys
import os

sys.path.append(os.path.dirname(__file__))

from pet_shop import PetShop
from io_strategy import FlaskIOStrategy
from storage import PickleStorage  

class App:
    def __init__(self, name):
        self.shop = PetShop(FlaskIOStrategy(), PickleStorage())
        self.app = Flask(name, 
                        template_folder='../../templates')
        self.app.secret_key = 'supersecretkey'
        self.register_routes()

    def register_routes(self):
        @self.app.route("/")
        def index():
            return render_template("akm2501/st11/index.html")

        @self.app.route("/create_animal", methods=["GET"])
        def create_animal():
            return render_template("akm2501/st11/create_animal.html")

        @self.app.route("/create_animal", methods=["POST"])
        def add_animal():
            message = self.shop.add_animal()  
            flash(message)
            return redirect(url_for("show_animals"))

        @self.app.route("/show_animals")
        def show_animals():
            animals = self.shop.show_catalog()
            return render_template("akm2501/st11/animals_list.html", animals=animals)

        @self.app.route("/edit_animal/<string:animal_id>", methods=["GET"])  
        def edit_animal(animal_id):
            animal = self.shop.get_by_id(animal_id)
            if not animal:
                flash("Животное не найдено")
                return redirect(url_for("show_animals"))
            return render_template("akm2501/st11/edit_animal.html", animal=animal)

        @self.app.route("/edit_animal/<string:animal_id>", methods=["POST"])  
        def confirm_edit(animal_id):
            message = self.shop.edit_animal(animal_id)  
            return redirect(url_for("show_animals"))

        @self.app.route("/delete_animal/<string:animal_id>")  
        def delete_animal(animal_id):
            message = self.shop.delete_animal(animal_id)
            flash(message)
            return redirect(url_for("show_animals"))

        @self.app.route("/dump")
        def dump():
            message = self.shop.save()  
            flash(message)
            return redirect(url_for("show_animals"))

        @self.app.route("/load")
        def load():
            message = self.shop.load()  
            flash(message)
            return redirect(url_for("show_animals"))

        @self.app.route("/clear")
        def clear():
            message = self.shop.clear_catalog()  
            flash(message)
            return redirect(url_for("show_animals"))

    def run(self):
        self.app.run(debug=True)