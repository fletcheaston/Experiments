
################################################################################
# Clean out files
clean:
	rm -rf .next
	rm -rf build
	rm -rf node_modules

# Setup of packages
node_modules: package.json package-lock.json
	npm install

	# Update timestamp
	touch -c node_modules

################################################################################
# Format
format: node_modules
	npm run format

# Lint
lint: node_modules
	npm run lint
	npm run type-check

################################################################################
# Run dev server locally
dev: node_modules
	poetry run python3 app.py
