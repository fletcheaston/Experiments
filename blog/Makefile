
################################################################################
# Shared vars
BLOG_STATIC = "build/static/"
BLOG_PAGES = "build/pages/"

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

# Build and copy over components
components: ../blog-components
	pushd ../blog-components && make build && popd
	cp -r ../blog-components/build/ docs/extras/

################################################################################
# Format
format: setup .
	poetry run isort .
	poetry run ruff format .

# Lint
lint: setup .
	poetry run ruff . --fix

################################################################################
# Run dev server locally
dev: setup
	poetry run mkdocs serve --dev-addr localhost:8000

# File setup for prod
build: setup
	# Run the build
	poetry run mkdocs build

	# Make local directory
	mkdir -p $(BLOG_STATIC)
	mkdir -p $(BLOG_PAGES)

	# Copy all files into /static and /pages
	cp -r build-raw/ $(BLOG_STATIC)
	cp -r build-raw/ $(BLOG_PAGES)

	# Delete all *.html files from static
	find $(BLOG_STATIC) -type f -name "*.html" -delete

	# Delete all non-*.html files from templates
	find $(BLOG_PAGES) -type f ! -name "*.html" -delete

	# Delete all empty directories
	find $(BLOG_STATIC) -empty -type d -delete
	find $(BLOG_PAGES) -empty -type d -delete

# Run prod server
prod: build
	 poetry run uvicorn app:app --proxy-headers --forwarded-allow-ips "*" --host 0.0.0.0 --port 8080
