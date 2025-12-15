#!/bin/bash
cd "${0%/*}"
source venv/bin/activate
export FLASK_APP=./app
flask run
