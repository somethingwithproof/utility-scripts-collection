"""Logging utilities for OpsForge."""

import logging
import sys
from pathlib import Path
from typing import Dict, Optional, Union


def setup_logging(
    log_level: Union[int, str] = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    log_format: Optional[str] = None,
    module_levels: Optional[Dict[str, Union[int, str]]] = None,
) -> None:
    """Configure logging with optional file output and per-module levels."""
    if isinstance(log_level, str):
        log_level = getattr(logging, log_level.upper())

    formatter = logging.Formatter(
        log_format or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    root = logging.getLogger()
    root.setLevel(log_level)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    root.addHandler(console)

    if log_file:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(path)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    if module_levels:
        for name, level in module_levels.items():
            if isinstance(level, str):
                level = getattr(logging, level.upper())
            logging.getLogger(name).setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
