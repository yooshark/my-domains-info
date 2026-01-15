.PHONY: lint format typecheck check

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy .

test:
	uv run coverage run -m pytest
	uv run coverage report

check: lint typecheck test
