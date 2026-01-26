import os
import yaml


class ConfigError(Exception):
    pass

class ConfigLoader:
    """
    ConfigLoader structure reused from:
    https://github.com/maru-bor/library_management_system/blob/master/db/config_loader.py
    """
    REQUIRED_STRUCTURE = {
        "bank": {
            "port": int,
        },
        "timeouts": {
            "command_timeout_sec": (int, float),
            "client_idle_timeout_sec": (int, float),
            "proxy_timeout_sec": (int, float),
        },
        "storage": {
            "data_file": str,
        },
        "logging": {
            "level": str,
            "file": str,
        },
    }

    @staticmethod
    def load_yaml_config(cfg_path: str) -> dict:
        """
        Reused/adapted from:
        throw-away67/portfolio database_project/src/config.py
        https://github.com/throw-away67/portfolio/blob/e39e2f5db7a140bc24f62d2430fdeac33b82d0c0/database_project/src/config.py
        """
        if not os.path.exists(cfg_path):
            raise ConfigError(f"Config file '{cfg_path}' not found")

        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigError(f"Invalid YAML format: {e}")

        if not isinstance(config, dict):
            raise ConfigError("Config must be a YAML mapping (dictionary)")

        ConfigLoader._validate(config)
        return config

    @staticmethod
    def _validate(config: dict):
        for section, keys in ConfigLoader.REQUIRED_STRUCTURE.items():
            if section not in config:
                raise ConfigError(f"ER Missing config section: '{section}'")
            section_value = config[section]
            if not isinstance(section_value, dict):
                raise ConfigError(f"ER Section '{section}' must be a mapping")

            for key, expected_type in keys.items():
                if key not in section_value:
                    raise ConfigError(f"ER Missing config key: '{section}.{key}'")

                value = section_value[key]

                if not isinstance(value, expected_type):
                    if isinstance(expected_type, tuple):
                        expected_names = ", ".join(t.__name__ for t in expected_type)
                        raise ConfigError(
                            f"ER Invalid type for '{section}.{key}', expected one of: {expected_names}"
                        )
                    else:
                        raise ConfigError(
                            f"ER Invalid type for '{section}.{key}', expected: {expected_type.__name__}"
                        )

                if isinstance(value, str) and not value.strip():
                    raise ConfigError(f"ER Config value '{section}.{key}' must not be empty")