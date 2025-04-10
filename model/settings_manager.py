import os
import json

class SettingsManager:
    def __init__(self, data_file="data/settings.json"):
        self.data_file = data_file
        self.entries = self._load_entries() or {}

    def get_setting(self, key):
        return self.entries.get(key, None)

    def set_setting(self, key, value):
        self.entries[key] = value

    def save_settings(self):
        self._save(self.entries)

    def _save(self, entries):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(entries, f, indent=2)

    def _load_entries(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
