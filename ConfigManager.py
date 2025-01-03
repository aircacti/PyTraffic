import os
import json

class ConfigManager:
    CONFIG_FILE = "config.json"
    DEFAULT_DOMAINS = ["example.com", "wp.pl"]

    def __init__(self):
        self.config_data = None

    def config_exists(self):
        return os.path.exists(self.CONFIG_FILE)

    def create_default_config(self):
        default_config = {"unsafe_domains": self.DEFAULT_DOMAINS}
        with open(self.CONFIG_FILE, "w") as config_file:
            json.dump(default_config, config_file, indent=4)
        self.config_data = default_config

    def load_config(self):
        try:
            with open(self.CONFIG_FILE, "r") as config_file:
                self.config_data = json.load(config_file)
                if not isinstance(self.config_data, dict) or "unsafe_domains" not in self.config_data:
                    raise ValueError("Invalid config file structure")
        except (json.JSONDecodeError, ValueError) as e:
            self.config_data = None
            raise RuntimeError(f"Error loading configuration: {e}")

    def get_unsafe_domains(self):
        if self.config_data:
            return self.config_data.get("unsafe_domains", [])
        return []

    def get_config_file_path(self):
        return os.path.abspath(self.CONFIG_FILE)

