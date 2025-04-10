import customtkinter as ctk
import tkinter as tk
import platform
import os
import sys

def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath("."), relative)

class TimeMateView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("TimeMate – Arbeitszeiterfassung")

        if platform.system() == "Windows":
            self.iconbitmap(resource_path("icons/timemate-green.ico"))
        else:
            self.iconphoto(False, tk.PhotoImage(file=resource_path("icons/timemate-green.png")))

        self.geometry("600x180")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.running = False
        self.last_visible_buttons = set()

        self.grid_rowconfigure(1, weight=1)

        #Menu Bar
        self.menu_frame = ctk.CTkFrame(self, bg_color="#000000")
        self.menu_frame.grid(row=0, column=0, sticky="e", padx=10, pady=(10, 0))

        self.menu_log_button = ctk.CTkButton(
            self.menu_frame,
            text="📄 Zeiterfassungen",
            command=self.controller.open_log_window,
            fg_color="gray",
            corner_radius=3,
            height=20
        )
        self.menu_log_button.grid(row=0, column=0, sticky="w")

        # Content frame
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=2)
        self.content_frame.grid_columnconfigure(2, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.display_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.display_frame.grid(row=0, column=0, sticky="ew")

        self.label = ctk.CTkLabel(self.display_frame, text="00:00:00", font=("Helvetica", 32), width=160, anchor="w")
        self.label.pack(anchor="w", pady=(15, 0))

        self.status_label = ctk.CTkLabel(self.display_frame, text="", font=("Helvetica", 11))
        self.status_label.pack(anchor="w", pady=0)

        shared_style = {
            "fg_color": "#2b2b2b",
            "border_color": "#3a3a3a",
            "border_width": 1,
            "corner_radius": 2,
            "text_color": "white",
            "width": 200
        }

        self.entry_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.entry_frame.grid(row=0, column=1, sticky="ew", padx=10)

        self.entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Projektname")
        self.entry.pack(pady=5)
        self.entry.configure(**shared_style)

        self.description = ctk.CTkTextbox(self.entry_frame, height=60)
        self.description.pack(pady=5)
        self.description.configure(**shared_style)

        self.placeholder_text = "Optionale Beschreibung hier eingeben..."
        self.description.insert("0.0", self.placeholder_text)
        self.description.configure(text_color="gray")
        self.description.bind("<FocusIn>", self._clear_placeholder)
        self.description.bind("<FocusOut>", self._restore_placeholder)

        self.button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.button_frame.grid(row=0, column=2, sticky="e", padx=10)

        self.start_button = ctk.CTkButton(self.button_frame, text="Start", command=self.controller.start_timer, fg_color="#3B82F6", hover_color="#2563EB", corner_radius=2)
        self.stop_button = ctk.CTkButton(self.button_frame, text="Stopp", command=self.controller.pause_timer, fg_color="#F59E0B", hover_color="#D97706", corner_radius=2)
        self.reset_button = ctk.CTkButton(self.button_frame, text="Abbrechen", command=self.controller.reset_timer, fg_color="#6B7280", hover_color="#4B5563", corner_radius=2)
        self.book_button = ctk.CTkButton(self.button_frame, text="Buchen", command=self.controller.book_time, fg_color="#10B981", hover_color="#059669", corner_radius=2)

        self.protocol("WM_DELETE_WINDOW", self.controller.hide_window)

        self.update_ui_loop()

        self.update_idletasks()
        self.deiconify()
        self.lift()
        self.focus_force()

    def format_seconds(self, seconds: int) -> str:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02}:{m:02}:{s:02}"

    def update_buttons(self, state):
        desired_buttons = set()

        if state["running"]:
            desired_buttons.add("stop")
        elif state["paused"]:
            desired_buttons.update(["start", "book", "reset"])
            self.start_button.configure(text="Fortsetzen")
        else:
            desired_buttons.add("start")
            self.start_button.configure(text="Start")

        if desired_buttons == self.last_visible_buttons:
            return

        self.last_visible_buttons = desired_buttons

        self.start_button.pack_forget()
        self.stop_button.pack_forget()
        self.book_button.pack_forget()
        self.reset_button.pack_forget()

        if "reset" in desired_buttons:
            self.reset_button.pack(pady=5)
        if "start" in desired_buttons:
            self.start_button.pack(pady=5)
        if "book" in desired_buttons:
            self.book_button.pack(pady=5)
        if "stop" in desired_buttons:
            self.stop_button.pack(pady=5)

    def update_from_session(self):
        state = {
            "running": self.controller.model.running,
            "paused": not self.controller.model.running and self.controller.model.start_time is not None,
            "elapsed": int(self.controller.model.get_duration().total_seconds())
        }
        self.running = state["running"]

        new_text = self.format_seconds(state["elapsed"])
        if getattr(self, "_last_label_text", None) != new_text:
            self.label.configure(text=new_text)
            self._last_label_text = new_text

        self.update_buttons(state)

    def update_ui_loop(self):
        self.update_from_session()
        self.after(1000, self.update_ui_loop)

    def update_timer_display(self, seconds):
        self.label.configure(text=self.format_seconds(seconds))

    def show_status(self, message):
        self.status_label.configure(text=message)

    def enable_booking(self):
        self.book_button.configure(state="normal")

    def disable_booking(self):
        self.book_button.configure(state="disabled")

    def _clear_placeholder(self, event=None):
        current = self.description.get("0.0", "end").strip()
        if current == self.placeholder_text:
            self.description.delete("0.0", "end")
            self.description.configure(text_color="white")

    def _restore_placeholder(self, event=None):
        current = self.description.get("0.0", "end").strip()
        if not current:
            self.description.insert("0.0", self.placeholder_text)
            self.description.configure(text_color="gray")