# Testing Guide for pyLumo

## Quick Start

```bash
# Install development dependencies (includes pytest + pytest-cov)
uv pip install -e ".[dev]"

# Run all tests
uv run pytest tests/

# Run a specific test file
uv run pytest tests/test_pylumo.py
```

**Note:** This project uses `uv` for dependency management. Always prefix commands with `uv run` to ensure dependencies are available.

## Test Suite Overview

### Unit Tests (`test_pylumo.py`)

Comprehensive automated tests covering all core functionality without requiring credentials or network access.

**Total: 32 tests across 9 categories**

#### 1. Encryption Tests (4 tests)
- ✅ PGP public key loading
- ✅ AES-256 key generation
- ✅ Encryption roundtrip verification
- ✅ PGP request key encryption

#### 2. Request Payload Tests (6 tests)
- ✅ Payload structure validation
- ✅ Tools configuration
- ✅ Targets configuration
- ✅ Turn structure
- ✅ Conversation history inclusion
- ✅ UUID request ID format

#### 3. Response Parsing Tests (5 tests)
- ✅ Token data event parsing
- ✅ Multiple target handling
- ✅ Invalid JSON line resilience
- ✅ Integrity verification failure stops processing and returns explicit error
- ✅ Integrity verification failure can raise for library-mode consumers

#### 4. File Upload Tests (4 tests)
- ✅ Text file formatting
- ✅ Binary file base64 encoding
- ✅ Image file handling
- ✅ Missing file error handling

#### 5. Conversation History Tests (3 tests)
- ✅ Empty initialization
- ✅ Clear history
- ✅ Max turns limit

#### 6. Session Management Tests (4 tests)
- ✅ Initial state
- ✅ Authentication flow (mocked)
- ✅ Logout functionality
- ✅ Session state transitions

#### 7. Proton TLS Pinning Tests (1 test)
- ✅ TLS pin regression check for `account.proton.me` (skipped if proton client not installed)

#### 8. Output File Tests (2 tests)
- ✅ Default None state
- ✅ File parameter handling

#### 9. Error Handling Tests (3 tests)
- ✅ Missing Proton API graceful failure
- ✅ Session save without active session
- ✅ Session load without Proton API

## Running Tests

### Run All Unit Tests

```bash
uv run pytest tests/
```

### Run Specific Test Category

```bash
# Run only encryption tests
uv run pytest tests/test_pylumo.py -k TestPyLumoEncryption

# Run only file upload tests
uv run pytest tests/test_pylumo.py -k TestPyLumoFileUpload
```

### Run Single Test

```bash
uv run pytest tests/test_pylumo.py -k test_pgp_key_loaded
```

### Verbose Output

```bash
uv run pytest tests/ -v
```

## Test Results

### Successful Run

```
test_aes_key_generation ... ok
test_encrypt_decrypt_roundtrip ... ok
test_pgp_key_loaded ... ok
[... 29 more tests ...]

----------------------------------------------------------------------
Ran 32 tests in 0.047s

OK

================================================================================
TEST SUMMARY
================================================================================
Tests run: 32
Successes: 32
Failures: 0
Errors: 0
================================================================================
```

### Understanding Warnings

You may see `CryptographyDeprecationWarning` messages from `pgpy`/`cryptography` on newer Python versions. These are warnings (not test failures) and are emitted by upstream dependencies.

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install uv
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH
      - name: Run tests
        run: uv run pytest tests/
```

## Writing New Tests

### Test Template

```python
import unittest
from pylumo import pyLumo

class TestNewFeature(unittest.TestCase):
    """Test description."""

    def setUp(self):
        """Set up test client."""
        self.client = pyLumo(quiet_mode=True)

    def test_feature_works(self):
        """Test that feature works correctly."""
        # Arrange
        expected = "expected_value"
        
        # Act
        result = self.client.some_method()
        
        # Assert
        self.assertEqual(result, expected)
```

### Best Practices

1. **Use descriptive names**: `test_encrypt_decrypt_roundtrip` not `test1`
2. **One assertion per test**: Keep tests focused
3. **Use setUp/tearDown**: Clean up resources
4. **Mock external dependencies**: Don't make real API calls in unit tests
5. **Test edge cases**: Empty strings, None values, invalid input
6. **Document expected behavior**: Use docstrings

## Troubleshooting

### Import Errors

```bash
# Ensure you're in the correct directory
cd /path/to/pylumo

# Check that uv is installed
uv --version

# Sync dependencies
uv sync
```

### Test Failures

1. **Check dependencies**: `uv sync`
2. **Verify Python version**: `python3 --version` (must be 3.12+)
3. **Run with verbose**: `uv run pytest tests/ -v`
4. **Check for file conflicts**: Ensure no stale `.pyc` files
5. **Always use uv run**: Don't run Python directly without `uv run`

### Debugging Tests

```python
# Add print statements
def test_something(self):
    result = self.client.method()
    print(f"Debug: result = {result}")  # Will show in test output
    self.assertEqual(result, expected)

# Use pdb debugger
import pdb; pdb.set_trace()  # Breakpoint
```

## Coverage Analysis

To measure test coverage:

```bash
# Ensure dev dependencies are installed (includes pytest-cov)
uv pip install -e ".[dev]"

# Run tests with coverage
uv run pytest tests/ --cov=pylumo

# Generate an HTML report
uv run pytest tests/ --cov=pylumo --cov-report=html
open htmlcov/index.html
```

## Contributing Tests

When adding new features:

1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain or improve coverage
4. Update this documentation
5. Run `python3 -m pyflakes test_pylumo.py` to check code quality

---

**Last Updated:** November 2025  
**Test Suite Version:** 1.0  
**Total Tests:** 32  
**Environment:** uv (Python 3.12+)
