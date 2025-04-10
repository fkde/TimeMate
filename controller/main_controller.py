import threading
import time
from model.session_manager import SessionManager
from view.main_view import TimeMateView
from view.modal.log_overview import LogOverviewModal
from view.modal.settings import SettingsModal
from model.settings_manager import SettingsManager
from view.tray_adapter import TrayIcon
from datetime import datetime, timedelta

class TimeMateController:
    def __init__(self):
        self.model = SessionManager()
        self.settings = SettingsManager()
        self.view = TimeMateView(self)
        self.tray = TrayIcon(self)
        self.timer_thread = None
        self.timer_running = False

    def start_timer(self):
        if not self.model.running:
            self.model.start()
            self.view.show_status("Timer läuft")
            self.timer_running = True
            self.timer_thread = threading.Thread(target=self._run_timer, daemon=True)
            self.timer_thread.start()
            self.view.update_from_session()
            self.tray.set_running(True)

    def reset_timer(self):
        if not self.model.running:
            self.model.reset()
            self.view.show_status("Timer zurückgesetzt")
            self.timer_running = False
            self.view.update_from_session()
            self.tray.set_running(False)

    def pause_timer(self):
        if self.model.running:
            self.model.pause()
            self.timer_running = False
            self.view.show_status("Timer pausiert")
            self.view.enable_booking()
            self.view.update_from_session()
            self.tray.set_running(False)

    def book_time(self):
        title = self.view.entry.get()
        description = self.view.description.get("0.0", "end").strip()
        if description == self.view.placeholder_text:
            description = ""
        entry = self.model.save_entry(title, description)
        self.view.show_status(f"Gebucht: {entry['duration']}")
        self.view.disable_booking()
        self.view.update_timer_display(0)
        self.view.update_from_session()
        self.tray.set_running(False)

        self.view.entry.delete(0, "end")
        self.view.description.delete("0.0", "end")
        self.view._restore_placeholder()

    def format_timestamp(self, timestamp_str):
        try:
            dt = datetime.fromisoformat(timestamp_str)
            return dt.strftime("%d.%m.%Y %H:%M:%S")
        except Exception:
            return timestamp_str

    def format_duration(self, seconds):
        try:
            return str(timedelta(seconds=int(seconds)))
        except Exception:
            return f"{seconds} s"

    def open_log_window(self):
        log_overview = LogOverviewModal(self)
        log_overview.grab_set()
        log_overview.wait_window()

    def open_settings_window(self):
        settings_modal = SettingsModal(self)
        settings_modal.deiconify()
        settings_modal.after(100, settings_modal.grab_set)
        settings_modal.wait_window()

    def save_settings(self, api_url):
        self.settings.set_setting("api_url", api_url)
        self.settings.save_settings()

    def _run_timer(self):
        while self.timer_running:
            duration = self.model.get_duration()
            seconds = int(duration.total_seconds())
            self.view.update_timer_display(seconds)
            time.sleep(1)

    def show_window(self):
        self.view.deiconify()
        self.view.focus()

    def hide_window(self):
        self.view.withdraw()

    def quit(self):
        self.timer_running = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=0.5)
        self.view.after(100, self.view.destroy)

    def run(self):
        self.view.mainloop()
