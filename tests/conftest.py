"""
Pytest configuration for pyLumo tests.

This file is loaded before any test modules, allowing us to configure
warning filters before pgpy is imported.
"""
import warnings

# Suppress CryptographyDeprecationWarning from pgpy for deprecated algorithms
# (IDEA, CAST5, Blowfish, TripleDES)
try:
    from cryptography.utils import CryptographyDeprecationWarning
    warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
except ImportError:
    pass
