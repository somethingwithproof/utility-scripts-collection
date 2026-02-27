"""
Common utilities and shared functions for the opsforge package.

This module provides shared functionality used across the different
modules, including configuration management, logging,
error handling, and other common utilities.
"""

from opsforge.common.config import ConfigManager
from opsforge.common.exceptions import (
    ConfigurationError,
    NetworkError,
    OpsForgeError,
    ValidationError,
)
from opsforge.common.logging import get_logger, setup_logging
