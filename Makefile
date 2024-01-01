
################################################################################
# Clean out files
clean:
	rm -rf .venv
	rm -rf build
	rm -rf .ruff_cache
	rm -rf .pytest_cache

	# Clean out all projects
	pushd advent-of-code && make clean && popd
	pushd blog && make clean && popd

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
format: .venv
	pushd advent-of-code && make format && popd
	pushd blog && make format && popd
	pushd my-freight-cube && make format && popd

# Lint
lint: .venv
	pushd advent-of-code && make lint && popd
	pushd blog && make lint && popd
	pushd my-freight-cube && make lint && popd

################################################################################
# Setup of pre-commit hooks
pre-commit-install: .venv .pre-commit-config.yaml
	poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg

# Run all pre-commit hooks
pre-commit-run: pre-commit-install
	poetry run pre-commit run --all
