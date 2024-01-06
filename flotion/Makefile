
################################################################################
# Clean out files
clean:
	rm -rf .next
	rm -rf build
	rm -rf node_modules

# Setup of packages
setup: package.json package-lock.json
	npm install

	# Update timestamp
	touch -c node_modules

################################################################################
# Format
format: setup
	npm run format

# Lint
lint: setup
	npm run lint
	npm run type-check

################################################################################
# Run dev server locally
dev: setup
	npm run dev
