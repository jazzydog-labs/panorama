# Panorama Development Tasks

# Run all tests with coverage
test:
    pytest --cov=. --cov-report=term-missing --cov-report=html --cov-fail-under=80

# Run full CI pipeline
ci: test format lint typecheck security

# Run all demo scripts
demo:
    python scripts/run_demos.py

# Format code with black
format:
    black .

# Lint code with ruff
lint:
    ruff check .

# Type check with mypy
typecheck:
    mypy .

# Security scan with bandit
security:
    bandit -r . -c pyproject.toml -f json -o bandit-report.json

# Install development dependencies
install:
    pip install -r requirements.txt
    pip install -r requirements-dev.txt

# Install pre-commit hooks
install-hooks:
    pre-commit install

# Run pre-commit on all files
pre-commit:
    pre-commit run --all-files

# Clean up generated files
clean:
    rm -rf __pycache__ .pytest_cache .coverage htmlcov .mypy_cache
    rm -f bandit-report.json
    find . -type d -name "*.egg-info" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete