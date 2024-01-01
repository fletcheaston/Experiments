
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

# Setup of virtual environment
setup: poetry.toml poetry.lock
	poetry lock
	poetry install --no-root

	# Update timestamp
	touch -c .venv

################################################################################
# Format
format: setup
	pushd advent-of-code && make format && popd
	pushd blog && make format && popd
	pushd blog-components && make format && popd
	pushd my-freight-cube && make format && popd

# Lint
lint: setup
	pushd advent-of-code && make lint && popd
	pushd blog && make lint && popd
	pushd blog-components && make lint && popd
	pushd my-freight-cube && make lint && popd

################################################################################
# Setup of pre-commit hooks
pre-commit-install: setup .pre-commit-config.yaml
	poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg

# Run all pre-commit hooks
pre-commit-run: pre-commit-install
	poetry run pre-commit run --all
