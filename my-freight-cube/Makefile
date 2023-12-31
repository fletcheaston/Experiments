
# Clean out files
clean:
	rm -rf .next
	rm -rf node_modules

# Format
format:
	npm run format

# Lint
lint:
	npm run lint

# Setup of packages
node_modules: package.json package-lock.json
	npm install

	# Update timestamp
	touch -c node_modules

# Run the project for local dev
dev: node_modules
	npm run dev

# Build the project for prod
build: node_modules .
	npm run build
