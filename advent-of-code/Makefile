
# Clean out files
clean:
	rm -rf .venv
	rm -rf build
	rm -rf .ruff_cache
	rm -rf .pytest_cache

# Format
format:
	poetry run isort .
	poetry run ruff format .

# Lint
lint:
	poetry run ruff . --fix

# Setup of virtual environment
.venv: poetry.toml pyproject.toml
	poetry lock
	poetry install --no-root

	# Update timestamp
	touch -c .venv

# Run all tests
test-all: .venv
	poetry run pytest . -n auto

# Run some tests
test-file: .venv
	poetry run pytest $(file) -s -vv -x
