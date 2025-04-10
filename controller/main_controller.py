import threading
import time
import customtkinter as ctk
from model.session_manager import SessionManager
from view.main_view import TimeMateView
from view.tray_adapter import TrayIcon
from datetime import datetime, timedelta


class TimeMateController:
    def __init__(self):
        self.model = SessionManager()
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
        log_window = ctk.CTkToplevel(self.view)
        log_window.title("Zeiterfassungen")
        log_window.geometry("500x400")

        scroll_frame = ctk.CTkScrollableFrame(log_window)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        def _on_mousewheel(event):
            scroll_frame._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        scroll_frame._parent_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Für Linux (Scrollrad wird anders übermittelt)
        scroll_frame._parent_canvas.bind_all("<Button-4>", lambda e: scroll_frame._parent_canvas.yview_scroll(-1, "units"))
        scroll_frame._parent_canvas.bind_all("<Button-5>", lambda e: scroll_frame._parent_canvas.yview_scroll(1, "units"))

        for entry in self.model.entries[::-1]:  # letzte zuerst
            start = self.format_timestamp(entry['start'])
            end = self.format_timestamp(entry['end'])
            duration = self.format_duration(entry['duration'])
            display = f"{start} → {end}\n{entry['title']} ({duration})\n{entry['description']}"
            label = ctk.CTkLabel(scroll_frame, text=display, anchor="w", justify="left")
            label.pack(fill="x", padx=5, pady=5)

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
