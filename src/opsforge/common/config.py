"""Configuration management for OpsForge."""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

from dotenv import load_dotenv
import yaml


logger = logging.getLogger(__name__)


class ConfigManager:
    """Loads config from environment variables and YAML files."""

    def __init__(
        self,
        config_file: Optional[Union[str, Path]] = None,
        env_prefix: str = "OPSFORGE_",
        load_env: bool = True,
    ):
        self.config: Dict[str, Any] = {}
        self.config_path: Optional[Path] = None

        if load_env:
            env_path = Path(".env")
            if env_path.exists():
                load_dotenv(env_path)

        self._load_from_env(env_prefix)

        if config_file:
            config_path = Path(config_file)
            if config_path.exists():
                self.config_path = config_path
                self._load_from_file(config_path)
            else:
                logger.warning(f"Config file not found: {config_file}")

    def _load_from_env(self, prefix: str) -> None:
        for key, value in os.environ.items():
            if key.startswith(prefix):
                parts = key[len(prefix) :].lower().split("_")
                current = self.config
                for part in parts[:-1]:
                    current = current.setdefault(part, {})
                current[parts[-1]] = value

    def _load_from_file(self, file_path: Path) -> None:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_config = yaml.safe_load(f)
                if file_config:
                    self._merge_configs(self.config, file_config)
        except Exception as e:
            logger.error(f"Error loading config: {e}")

    def _merge_configs(self, base: Dict, overlay: Dict) -> None:
        for key, value in overlay.items():
            if (
                key in base
                and isinstance(base[key], dict)
                and isinstance(value, dict)
            ):
                self._merge_configs(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value. Supports dot notation (e.g., 'database.host')."""
        parts = key.split(".")
        current = self.config
        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return default
            current = current[part]
        return current

    def set(self, key: str, value: Any) -> None:
        """Set config value. Supports dot notation."""
        parts = key.split(".")
        current = self.config
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = value

    def save(self, file_path: Optional[Union[str, Path]] = None) -> None:
        """Save config to YAML file."""
        save_path = Path(file_path) if file_path else self.config_path
        if not save_path:
            logger.error("No file path specified")
            return
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                yaml.dump(self.config, f, default_flow_style=False)
        except Exception as e:
            logger.error(f"Error saving config: {e}")
