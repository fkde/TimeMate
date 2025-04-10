import customtkinter as ctk
from Xlib.Xcursorfont import bottom_side

from model.session_manager import SessionManager

class LogOverviewModal(ctk.CTkToplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Zeiterfassungen")
        self.geometry("300x400")

        # Erstelle das Scroll-Frame
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Mausrad zum Scrollen
        def _on_mousewheel(event):
            scroll_frame._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        scroll_frame._parent_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Für Linux (Scrollrad wird anders übermittelt)
        scroll_frame._parent_canvas.bind_all("<Button-4>", lambda e: scroll_frame._parent_canvas.yview_scroll(-1, "units"))
        scroll_frame._parent_canvas.bind_all("<Button-5>", lambda e: scroll_frame._parent_canvas.yview_scroll(1, "units"))

        # Zeige die Log-Einträge
        for entry in self.controller.model.entries[::-1]:  # letzte zuerst
            start = self.controller.format_timestamp(entry['start'])
            end = self.controller.format_timestamp(entry['end'])
            duration = self.controller.format_duration(entry['duration'])
            display = f"{start} → {end}\n({duration})\n{entry['title']}\n{entry['description']}"

            label = ctk.CTkLabel(scroll_frame, text=display, anchor="w", justify="left")
            label.pack(fill="x", padx=5, pady=5)

