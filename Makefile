help:
	@echo "Available targets:"
	@echo "  test-db      - Test database connection using main.py"
	@echo "  format       - Format code with ruff"
	@echo "  lint         - Lint code with ruff"
	@echo "  lint-fix     - Fix linting issues automatically"
	@echo "  help         - Show this help message"


test-db:
	@echo "Testing database connection..."
	python main.py

format:
	@echo "Formatting code with ruff..."
	ruff format .

lint:
	@echo "Linting code with ruff..."
	ruff check .

lint-fix:
	@echo "Fixing linting issues..."
	ruff check --fix .
