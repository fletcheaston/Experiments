
################################################################################
# Clean out files
clean:
	rm -rf .venv
	rm -rf build
	rm -rf .ruff_cache
	rm -rf .pytest_cache

# Setup of virtual environment
setup: poetry.toml poetry.lock
	poetry lock
	poetry install --no-root

	# Update timestamp
	touch -c .venv

################################################################################
# Format
format: setup
	poetry run isort .
	poetry run ruff format .

# Lint
lint: setup
	poetry run ruff . --fix

# Run all tests
test-all: setup
	poetry run pytest . -n auto

# Run some tests
test-file: setup
	poetry run pytest $(file) -s -vv -x

################################################################################
# Run dev server locally
dev: setup
	poetry run python3 app.py
