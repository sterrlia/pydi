install:
	poetry install --no-interaction --no-root

test:
	@poetry run python -m nose2
