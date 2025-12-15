@echo off
cd /d %~dp0

if exist venv\ (
	call venv\scripts\activate.bat
) else (
	python -m venv venv
	call venv\scripts\activate.bat
	pip3 install -r requirements.txt
)	

start python lab4client.py
