
################################################################################
# Shared vars
BLOG_STATIC = "app_blog/static/blog/"
BLOG_TEMPLATES = "app_blog/templates/"

MFC_STATIC = "app_my_freight_cube/static/my-freight-cube/"
MFC_TEMPLATES = "app_my_freight_cube/templates/"


################################################################################
# Clean out files
clean:
	rm -rf .venv
	rm -rf build
	rm -rf .ruff_cache
	rm -rf .pytest_cache

	# Other project files
	rm -rf $(BLOG_STATIC)
	rm -rf $(BLOG_TEMPLATES)

	rm -rf $(MFC_STATIC)
	rm -rf $(MFC_TEMPLATES)

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

# Run database for local development
database:
	docker-compose up

################################################################################
# Blog file setup
build-blog:
	# Make local directory
	mkdir -p $(BLOG_STATIC)
	mkdir -p $(BLOG_TEMPLATES)

	# Build blog
	pushd ../blog && make build && popd

	# Copy all files into /static and /templates
	cp -r ../blog/build/ $(BLOG_STATIC)
	cp -r ../blog/build/ $(BLOG_TEMPLATES)

	# Delete all *.html files from static
	find $(BLOG_STATIC) -type f -name "*.html" -delete

	# Delete all non-*.html files from templates
	find $(BLOG_TEMPLATES) -type f ! -name "*.html" -delete

	# Delete all empty directories
	find $(BLOG_STATIC) -empty -type d -delete
	find $(BLOG_TEMPLATES) -empty -type d -delete

################################################################################
# Blog file setup
build-my-freight-cube:
	# Make local directory
	mkdir -p $(MFC_STATIC)
	mkdir -p $(MFC_TEMPLATES)

	# Build my-freight-cube
	pushd ../my-freight-cube && make build && popd

	# Copy all files into /static and /templates
	cp -r ../my-freight-cube/build/ $(MFC_STATIC)
	cp -r ../my-freight-cube/build/ $(MFC_TEMPLATES)

	# Delete all *.html and *.txt files from static
	find $(MFC_STATIC) -type f -name "*.html" -delete
	find $(MFC_STATIC) -type f -name "*.txt" -delete

	# Delete all non-*.html/*.txt files from templates
	find $(MFC_TEMPLATES) -type f ! -name "*.html" ! -name "*.txt" -delete

	# Delete all empty directories
	find $(MFC_STATIC) -empty -type d -delete
	find $(MFC_TEMPLATES) -empty -type d -delete


# Run app for local development
dev: .venv build-blog build-my-freight-cube
	poetry run python3 manage.py collectstatic --no-input
	poetry run python3 manage.py runserver localhost:8000
