import customtkinter as ctk
import platform
import tkinter as tk
import os
import sys

from tray_adapter import TrayAdapter
from tray_adapter import resource_path

tray = TrayAdapter()
tray.run()

class TimeMateGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TimeMate – Arbeitszeiterfassung")

        # 🧠 Custom Window-Icon setzen
        if platform.system() == "Windows":
            self.iconbitmap(resource_path("icons/timemate-green.ico"))
        else:
            self.iconphoto(False, tk.PhotoImage(file=resource_path("icons/timemate-green.png")))


        self.geometry("600x150")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        tray.register_gui(self)
        self.running = False
        self.last_state = None
        self.last_visible_buttons = set()

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=2)
        self.content_frame.grid_columnconfigure(2, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.display_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.display_frame.grid(row=0, column=0, sticky="ew")

        self.label = ctk.CTkLabel(self.display_frame, text="00:00:00", font=("Helvetica", 32))
        self.label.pack(anchor="w", pady=(15, 0))

        # Statuszeile (darunter)
        self.status_label = ctk.CTkLabel(self.display_frame, text="", font=("Helvetica", 12))
        self.status_label.pack(anchor="w", pady=(0,0))

        # EntryFrame (Nutzereingaben)

        shared_style = {
            "fg_color": "#2b2b2b",  # Hintergrund (z. B. dunkler grau)
            "border_color": "#3a3a3a",  # Rahmenfarbe
            "border_width": 1,
            "corner_radius": 6,  # schön abgerundet wie Entry
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

        self.start_button = ctk.CTkButton(self.button_frame, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = ctk.CTkButton(self.button_frame, text="Pause", command=self.pause_timer)
        self.stop_button.pack(pady=5)

        self.reset_button = ctk.CTkButton(self.button_frame, text="Abbrechen", command=self.reset_timer)
        self.reset_button.pack(pady=5)

        self.book_button = ctk.CTkButton(self.button_frame, text="Buchen", command=self.book_session)
        self.book_button.pack(pady=5)

        self.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.update_ui_loop()

        self.deiconify()
        self.lift()
        self.focus_force()

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

    def start_timer(self):
        tray.start_timer()
        self.status_label.configure(text="Timer gestartet", text_color="gray")

    def pause_timer(self):
        tray.pause_timer()
        self.status_label.configure(text="Timer pausiert", text_color="orange")

    def reset_timer(self):
        tray.reset_timer()
        self.status_label.configure(text="Timer abgebrochen", text_color="gray")

    def book_session(self):
        tray.book_session(self.entry.get(), self.description.get("0.0", "end").strip())
        self.status_label.configure(text="Session gespeichert ✔", text_color="green")
        self.entry.delete(0, ctk.END)
        self.description.delete("0.0", "end")

    def update_buttons(self, state):
        desired_buttons = set()

        if state["running"]:
            desired_buttons.add("stop")
            self.stop_button.configure(text="Pause")
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

        if "start" in desired_buttons:
            self.start_button.pack(pady=5)
        if "stop" in desired_buttons:
            self.stop_button.pack(pady=5)
        if "book" in desired_buttons:
            self.book_button.pack(pady=5)
        if "reset" in desired_buttons:
            self.reset_button.pack(pady=5)

    def update_from_session(self):
        state = tray.get_session_state()
        self.running = state["running"]

        new_text = self.format_seconds(state["elapsed"])
        if getattr(self, "_last_label_text", None) != new_text:
            self.label.configure(text=new_text)
            #self._last_label_text = new_text

        self.update_buttons(state)

    def update_ui_loop(self):
        self.update_from_session()
        self.after(1000, self.update_ui_loop)

    def hide_window(self):
        self.withdraw()

    def format_seconds(self, secs):
        h = secs // 3600
        m = (secs % 3600) // 60
        s = secs % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

if __name__ == "__main__":
    # Lock setzen
    lockfile = "/tmp/timemate.lock"
    if os.path.exists(lockfile):
        print("❗ TimeMate läuft bereits.")
        sys.exit()

    with open(lockfile, "w") as f:
        f.write(str(os.getpid()))

    try:
        app = TimeMateGUI()
        app.mainloop()
    finally:
        # Lock entfernen – auch bei Absturz / Schließen
        if os.path.exists(lockfile):
            os.remove(lockfile)



