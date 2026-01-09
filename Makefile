.PHONY: install install-tui install-dev install-all uninstall clean test help

 PYTHON ?= python3
 VENV ?= .venv
 VENV_PY := $(VENV)/bin/python

help:
	@echo "pylumo - Makefile commands"
	@echo ""
	@echo "Installation:"
	@echo "  make install      - Install CLI only"
	@echo "  make install-tui  - Install with TUI support (recommended)"
	@echo "  make install-dev  - Install with development tools"
	@echo "  make install-all  - Install everything"
	@echo ""
	@echo "Maintenance:"
	@echo "  make uninstall    - Uninstall pylumo and dependencies"
	@echo "  make clean        - Remove build artifacts and cache"
	@echo "  make test         - Run tests"
	@echo ""
	@echo "Requirements:"
	@echo "  - Python 3.12+"
	@echo "  - GnuPG (brew install gnupg)"
	@echo "  - uv package manager"

check-python:
	@$(PYTHON) -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" || (echo "Error: Python 3.12+ is required. Current: $$($(PYTHON) --version 2>&1)"; exit 1)

venv: $(VENV_PY)

$(VENV_PY):
	@$(PYTHON) -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" || (echo "Error: Python 3.12+ is required. Current: $$($(PYTHON) --version 2>&1)"; exit 1)
	@uv venv --python 3.12 $(VENV)

install: check-python venv
	@$(VENV_PY) scripts/install.py

install-tui: check-python venv
	@$(VENV_PY) scripts/install.py --tui

install-dev: check-python venv
	@$(VENV_PY) scripts/install.py --dev

install-all: check-python venv
	@$(VENV_PY) scripts/install.py --all

uninstall:
	@$(PYTHON) scripts/uninstall.py

clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info .eggs/
	@rm -rf .pytest_cache/ .coverage htmlcov/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@echo "✓ Clean complete"

test: $(VENV_PY)
	@uv sync --all-extras
	@$(VENV_PY) -m pytest tests/ -v || $(VENV_PY) -W "ignore::DeprecationWarning" -m unittest

upgrade-python:
	@./upgrade_python.sh

.DEFAULT_GOAL := help
