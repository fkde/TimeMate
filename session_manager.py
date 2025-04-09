import time
import json
import os
from datetime import datetime

DATA_FILE = "sessions.json"

class SessionManager:
    def __init__(self):
        self.running = False
        self.paused = False
        self.start_time = None
        self.elapsed = 0

    def start(self):
        if not self.running:
            if self.paused:
                # Fortsetzen nach Pause
                self.start_time = time.time() - self.elapsed
                self.running = True
                self.paused = False
                print("Timer fortgesetzt")
            else:
                # Ganz neu starten
                self.start_time = time.time()
                self.running = True
                self.paused = False
                self.elapsed = 0
                print("Timer gestartet")

    def pause(self):
        if self.running:
            self.running = False
            self.paused = True
            self.elapsed = int(time.time() - self.start_time)
            print("Timer gestoppt")

    def reset(self):
        if not self.running:
            self.paused = False
            self.elapsed = 0
            print("Timer zurückgesetzt")

    def book(self, text="", description=""):
        if not self.paused:
            return

        end_time = self.start_time + self.elapsed
        session = {
            "start": datetime.fromtimestamp(self.start_time).isoformat(),
            "end": datetime.fromtimestamp(end_time).isoformat(),
            "title": text,
            "description": description,
            "duration_seconds": self.elapsed
        }

        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump([], f)

        with open(DATA_FILE, "r+") as f:
            data = json.load(f)
            data.append(session)
            f.seek(0)
            json.dump(data, f, indent=2)

        self.start_time = None
        self.paused = False
        self.elapsed = 0
        print("Session gebucht")

    def get_elapsed(self):
        if self.running:
            return int(time.time() - self.start_time)
        elif self.paused:
            return self.elapsed
        return 0

    def get_state(self):
        return {
            "running": self.running,
            "paused": self.paused,
            "elapsed": self.get_elapsed()
        }
