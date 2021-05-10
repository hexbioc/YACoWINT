SHELL = /bin/bash

.ONESHELL:

.PHONY: init
init:
	@python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt
	pre-commit install

format:
	@. venv/bin/activate
	isort -rc server/
	black server/

lint:
	@. venv/bin/activate
	flake8 server/

local.database:
	@. .envrc
	docker-compose run -p"5432:5432" database

local.server:
	@. venv/bin/activate
	. .envrc
	uvicorn --reload --port 8080 "server.app:app"

services:
	@. .envrc
	docker-compose up --build -d
