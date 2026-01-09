# Contributing to pyLumo

Thank you for your interest in contributing to pyLumo! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We welcome contributors of all experience levels.

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- GnuPG (`brew install gnupg` on macOS)

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Mindgard/pylumo.git
   cd pylumo
   ```

2. Install development dependencies:
   ```bash
   make install-all
   ```
   
   Or manually:
   ```bash
   uv sync --all-extras
   ```

3. Run tests to verify setup:
   ```bash
   make test
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
make test

# Run with pytest directly
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_pylumo.py -v

# Run with coverage
uv run pytest tests/ --cov=pylumo

# Generate HTML coverage report
uv run pytest tests/ --cov=pylumo --cov-report=html
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Add docstrings to public functions and classes
- Keep lines under 88 characters (Black default)

### Linting

```bash
uv run pyflakes src/pylumo/
```

## Making Changes

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add support for new Lumo tool
fix: handle 2FA timeout correctly
docs: update installation instructions
refactor: simplify encryption logic
```

### Pull Requests

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Add/update tests as needed
5. Ensure all tests pass
6. Update documentation if applicable
7. Submit a pull request

#### PR Checklist

- [ ] Tests pass (`make test`)
- [ ] Code follows project style
- [ ] Documentation updated (if applicable)
- [ ] CHANGELOG.md updated (for user-facing changes)
- [ ] Commit messages are clear

## Project Structure

```
pylumo/
├── src/pylumo/           # Main package
│   ├── __init__.py       # Package exports and version
│   ├── pylumo.py         # Core client
│   ├── pylumo_tui.py     # Terminal UI
│   ├── _pylumo_debug.py  # Debug client
│   ├── _pylumo_config.py # Configuration manager
│   └── _pylumo_tui_modals.py  # TUI modal dialogs
├── tests/                # Test suite
├── docs/                 # Documentation
├── scripts/              # Installation scripts
└── pyproject.toml        # Project configuration
```

## Reporting Issues

When reporting bugs, please include:

- Python version (`python --version`)
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Relevant error messages or logs

## Security

If you discover a security vulnerability, please email security@mindgard.ai instead of opening a public issue.

## License

By contributing, you agree that your contributions will be licensed under the GPL-3.0-or-later license.

## Questions?

Open a [GitHub Discussion](https://github.com/Mindgard/pylumo/discussions) or reach out to the maintainers.
