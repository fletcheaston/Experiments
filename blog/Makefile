
################################################################################
# Clean out files
clean:
	rm -rf .venv
	rm -rf build
	rm -rf .ruff_cache
	rm -rf .pytest_cache

# Setup of poetry lockfile
poetry.lock: pyproject.toml
	test -f poetry.lock || poetry lock

	# Update timestamp
	touch -c poetry.lock

# Setup of virtual environment
.venv: poetry.toml poetry.lock
	poetry install --no-root

	# Update timestamp
	touch -c .venv

################################################################################
# Format
format: .venv .
	poetry run isort .
	poetry run ruff format .

# Lint
lint: .venv .
	poetry run ruff . --fix

################################################################################
# Run dev server locally
dev: .venv
	poetry run python3 app.py
