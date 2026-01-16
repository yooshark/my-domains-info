.PHONY: lint format typecheck check

lint:
	uv run ruff check app

format:
	uv run ruff format .

typecheck:
	uv run mypy app

test:
	uv run coverage run -m pytest
	uv run coverage report
	uv run coverage xml

check: lint typecheck test
