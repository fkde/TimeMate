import datetime
import os
import json
from model.settings_manager import SettingsManager
import requests

class SessionManager:
    def __init__(self, data_file="data/sessions.json"):
        self.running = False
        self.start_time = None
        self.last_stop_time = None
        self.accumulated_duration = datetime.timedelta(0)
        self.entries = []
        self.data_file = data_file
        self._load_entries()
        self.api_url = None
        self.api_token = None

    def start(self):
        if not self.running:
            self.start_time = datetime.datetime.now()
            self.running = True

    def pause(self):
        if self.running:
            now = datetime.datetime.now()
            self.accumulated_duration += now - self.start_time
            self.last_stop_time = now
            self.running = False

    def reset(self):
        self.start_time = None
        self.last_stop_time = None
        self.accumulated_duration = datetime.timedelta(0)
        self.running = False

    def get_duration(self):
        if self.running and self.start_time:
            return self.accumulated_duration + (datetime.datetime.now() - self.start_time)
        return self.accumulated_duration

    def save_entry(self, title="", description=""):
        end_time = self.last_stop_time or datetime.datetime.now()
        entry = {
            "start": self.start_time.isoformat() if self.start_time else end_time.isoformat(),
            "end": end_time.isoformat(),
            "duration": int(self.get_duration().total_seconds()),
            "title": title,
            "description": description
        }
        self.entries.append(entry)
        self._save_entries()
        self.reset()

        settings_manager = SettingsManager()
        self.api_url = settings_manager.get_setting("api_url")
        self.api_token = settings_manager.get_setting("api_token")

        if self.api_url:
            headers = {
                "X-Client": "TimeMate v1.0"
            }
            try:
                if self.api_token:
                    headers["Authorization"] = f"Bearer {self.api_token}"

                response = requests.post(self.api_url, json=entry, headers=headers)
                response.raise_for_status()
            except Exception as e:
                print("❌ API-Fehler:", e)

        return entry

    def _save_entries(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.entries, f, indent=2)

    def _load_entries(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.entries = json.load(f)

