# Setup Development Infrastructure

## Story
As a developer working on Panorama, I would like to have a complete development infrastructure with automated tasks, testing framework, and CI/CD pipeline so that I can efficiently develop, test, and maintain the codebase with confidence.

## Acceptance Criteria
- [x] Create a `justfile` with all necessary development tasks
- [x] Set up pytest as the testing framework with proper configuration
- [x] Create GitHub Actions workflow for CI/CD pipeline
- [x] Add pre-commit hooks for code quality
- [x] Configure code formatting (black), linting (ruff), and type checking (mypy)
- [x] Create demo scripts directory structure
- [x] All `just` commands work as documented in CLAUDE.md

## High-Level Design
1. **Justfile Creation**: Implement all commands mentioned in CLAUDE.md (test, ci, demo)
2. **Testing Infrastructure**: Migrate from basic assertions to pytest framework
3. **CI/CD Pipeline**: GitHub Actions workflow that runs on push/PR
4. **Code Quality Tools**: Pre-commit config with black, ruff, mypy
5. **Demo Framework**: Scripts directory with runner for demonstrations

## Low-Level Design
1. **justfile**:
   ```
   - test: Run pytest with coverage report
   - ci: Run tests + format + lint + typecheck + security
   - demo: Execute all demo scripts
   - format: Run black
   - lint: Run ruff
   - typecheck: Run mypy
   - security: Run bandit
   ```

2. **pytest configuration** (pyproject.toml):
   - Coverage settings (>80% requirement)
   - Test discovery patterns
   - Fixtures for common test scenarios

3. **GitHub Actions** (.github/workflows/ci.yml):
   - Trigger on push and PR
   - Matrix testing for Python versions
   - Run full CI pipeline
   - Coverage reporting

4. **Pre-commit hooks** (.pre-commit-config.yaml):
   - Black formatting
   - Ruff linting
   - Mypy type checking
   - YAML validation

5. **Demo structure**:
   - scripts/demos/README.md
   - scripts/demos/basic_collection.py
   - scripts/run_demos.py

## Definition of Done
- [x] `just test` runs pytest with coverage report showing >80%
- [x] `just ci` successfully runs all quality checks
- [x] `just demo` executes demo scripts without errors
- [x] GitHub Actions workflow passes on a test PR
- [x] Pre-commit hooks are installable and functional
- [x] All existing tests are migrated to pytest
- [x] Development setup is documented in README.md

## Status: COMPLETED ✓