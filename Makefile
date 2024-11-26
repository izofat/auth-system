SHELL := /bin/bash
PROJECT_NAME := auth-system

POETRY := ~/.local/bin/poetry

launch:
	@poetry run python main.py

install:
	@poetry install
	@poetry run mypy --install-types

format:
	@poetry run autoflake --in-place --remove-all-unused-imports --recursive --remove-unused-variables \
		--ignore-init-module-imports .
	@poetry run isort .
	@poetry run black .

type-check:
	@poetry run mypy auth_system
	@poetry run mypy tests

lint:
	@poetry run pylint auth_system
	@poetry run pylint tests
	@poetry run bandit -r auth_system

test-db:
	@poetry run pytest tests/db