.PHONY: lint format typecheck check

lint:
	ruff check app

format:
	ruff format .

typecheck:
	uv run mypy app

test:
	uv run coverage run -m pytest
	uv run coverage report

check: lint typecheck test
