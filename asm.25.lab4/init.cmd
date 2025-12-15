@echo off
cd /d %~dp0

python -m venv venv
call venv\scripts\activate.bat
pip3 install flask
pip3 install requests
pip3 install legacy-cgi
pip3 freeze > requirements.txt
