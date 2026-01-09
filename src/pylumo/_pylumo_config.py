"""Configuration manager for pyLumo TUI application.

Handles loading, saving, and managing application configuration and state.
"""

import json
import os
import tempfile
import keyring
from pathlib import Path
from typing import Any, Optional


class ConfigManager:
    """Manages unified configuration for pyLumo TUI."""

    CONFIG_VERSION = "1.0"
    CONFIG_FILENAME = "config.json"

    def __init__(self, app_dir: Path):
        """Initialize config manager.

        Args:
            app_dir: Application directory path
        """
        self.app_dir = Path(app_dir)
        self.config_file = self.app_dir / self.CONFIG_FILENAME
        self._config = self._get_default_config()
        self._load_config()

    def _get_default_config(self) -> dict:
        """Get default configuration structure."""
        return {
            "version": self.CONFIG_VERSION,
            "auth": {"session_data": None},
            "preferences": {"enabled_tools": [], "theme": "default"},
            "security": {"tls_pinning": True},
            "app_state": {},
        }

    def _load_config(self) -> None:
        """Load configuration from file."""
        if not self.config_file.exists():
            # Create default config if it doesn't exist
            self._save_config()
            return

        try:
            with open(self.config_file, "r") as f:
                loaded_config = json.load(f)

            # Merge with defaults to ensure all keys exist
            self._config = self._merge_with_defaults(loaded_config)

        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load config: {e}. Using defaults.")
            self._config = self._get_default_config()
            self._save_config()

    def _merge_with_defaults(self, loaded: dict) -> dict:
        """Merge loaded config with defaults to ensure all keys exist."""
        defaults = self._get_default_config()

        def merge_dicts(default: dict, loaded: dict) -> dict:
            result = default.copy()
            for key, value in loaded.items():
                if (
                    key in result
                    and isinstance(result[key], dict)
                    and isinstance(value, dict)
                ):
                    result[key] = merge_dicts(result[key], value)
                else:
                    result[key] = value
            return result

        return merge_dicts(defaults, loaded)

    def _save_config(self) -> None:
        """Save configuration to file atomically."""
        try:
            # Ensure directory exists
            self.app_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
            try:
                os.chmod(self.app_dir, 0o700)
            except Exception:
                pass

            fd: Optional[int] = None
            tmp_path: Optional[str] = None
            try:
                fd, tmp_path = tempfile.mkstemp(
                    prefix=".pylumo-config-",
                    dir=str(self.app_dir),
                    text=True,
                )
                try:
                    os.fchmod(fd, 0o600)
                except Exception:
                    pass

                with os.fdopen(fd, "w") as f:
                    fd = None
                    json.dump(self._config, f, indent=2)

                os.replace(tmp_path, self.config_file)
                try:
                    os.chmod(self.config_file, 0o600)
                except Exception:
                    pass
            finally:
                if fd is not None:
                    try:
                        os.close(fd)
                    except Exception:
                        pass
                if tmp_path is not None and os.path.exists(tmp_path):
                    try:
                        os.unlink(tmp_path)
                    except Exception:
                        pass

        except IOError as e:
            print(f"Warning: Failed to save config: {e}")

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.

        Args:
            key_path: Dot-separated path to the config value (e.g., "auth.username")
            default: Default value if key doesn't exist

        Returns:
            Configuration value or default
        """
        keys = key_path.split(".")
        value = self._config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path: str, value: Any) -> None:
        """Set a configuration value using dot notation.

        Args:
            key_path: Dot-separated path to the config value (e.g., "auth.username")
            value: Value to set
        """
        keys = key_path.split(".")
        config = self._config

        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        # Set the value
        config[keys[-1]] = value

        # Save immediately
        self._save_config()

    def get_session_data(self) -> Optional[dict]:
        """Get session data for pyLumo client.

        Returns:
            Session data dict or None
        """
        return self.get("auth.session_data")

    def set_session_data(self, session_data: Optional[dict]) -> None:
        """Set session data from pyLumo client.

        Args:
            session_data: Session data dict or None to clear
        """
        self.set("auth.session_data", session_data)

    def clear_session(self) -> None:
        """Clear authentication session data."""
        self.set("auth.session_data", None)

    def get_username(self) -> str:
        """Get saved username from keychain.

        Returns:
            Username string (empty if not set or keychain unavailable)
        """
        try:
            username = keyring.get_password("pylumo", "saved_username")
            return username if username else ""
        except Exception:
            return ""

    def set_username(self, username: str) -> None:
        """Set username in keychain.

        Args:
            username: Username to save
        """
        try:
            if username:
                keyring.set_password("pylumo", "saved_username", username)
            else:
                # Clear username if empty
                try:
                    keyring.delete_password("pylumo", "saved_username")
                except keyring.errors.PasswordDeleteError:
                    pass  # Already deleted or doesn't exist
        except Exception:
            pass  # Silently fail if keychain unavailable

    def get_enabled_tools(self) -> list[str]:
        """Get list of enabled tools.

        Returns:
            List of enabled tool names
        """
        return self.get("preferences.enabled_tools", [])

    def set_enabled_tools(self, tools: list[str]) -> None:
        """Set enabled tools list.

        Args:
            tools: List of tool names to enable
        """
        self.set("preferences.enabled_tools", tools)

    def get_tls_pinning(self) -> bool:
        """Get TLS pinning setting.

        Returns:
            True if TLS pinning is enabled (default), False otherwise
        """
        return self.get("security.tls_pinning", True)

    def set_tls_pinning(self, enabled: bool) -> None:
        """Set TLS pinning setting.

        Args:
            enabled: True to enable TLS pinning, False to disable
                WARNING: Disabling TLS pinning reduces security.
                Only disable if behind a corporate proxy/VPN with SSL inspection.
        """
        self.set("security.tls_pinning", enabled)
