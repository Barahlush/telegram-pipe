SHELL := /bin/bash -O globstar

lint:
	@echo
	ruff .
	@echo
	blue --check --diff --color .
	@echo
	mypy .
	@echo
	pip-audit


format:
	ruff --silent --exit-zero --fix .
	blue .

install:
	poetry install

run:
	poetry run python3 telegram_pipe/client.py

install_hooks:
	@ scripts/install_hooks.sh
