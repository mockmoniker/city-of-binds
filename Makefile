.PHONY: help clean install build test lint format deploy deploy-test check

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

clean:  ## Remove build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find CityOfBinds tests -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find CityOfBinds tests -type f -name "*.pyc" -delete 2>/dev/null || true

install:  ## Install package in development mode
	pip install -e .[dev]

build: clean  ## Build source and wheel distributions
	python -m build

test:  ## Run tests
	pytest

lint:  ## Run linting tools
	black --check .
	isort --check-only .
	mypy .

format:  ## Format code with black and isort
	black .
	isort .

check: build  ## Validate package for PyPI upload
	twine check dist/*

deploy-test: check  ## Deploy to TestPyPI
	twine upload --repository testpypi dist/*

deploy: check  ## Deploy to PyPI
	twine upload dist/*

# Development workflow targets
dev-setup:  ## Set up development environment
	pip install -e .[dev]

release: clean lint test build check  ## Full release workflow (build + validate, but don't upload)
	@echo "✅ Release ready! Run 'make deploy-test' or 'make deploy' to upload."