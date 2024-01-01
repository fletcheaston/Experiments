
# Clean out files
clean:
	rm -rf build

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

# Run the project for local dev
dev: .venv
	poetry run mkdocs serve --dev-addr localhost:8001

# Build the project for prod
build: .venv .
	poetry run mkdocs build --strict
