import customtkinter as ctk
from model.session_manager import SessionManager

class SettingsModal(ctk.CTkToplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Einstellungen")
        self.geometry("400x400")

        # Erstelle das Scroll-Frame
        scroll_frame = ctk.CTkFrame(self, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        storage_input_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        storage_input_frame.grid(row=0, column=0, sticky="new", padx=0, pady=0)

        # Storage
        storage_label = ctk.CTkLabel(storage_input_frame, text="Nutze URL-Endpunkt:")

        self.storage_check_var = ctk.BooleanVar()
        self.storage_input = ctk.CTkEntry(storage_input_frame, placeholder_text="URL-Endpunkt", width=200)
        self.storage_checkbox = ctk.CTkCheckBox(storage_input_frame, width=40, variable=self.storage_check_var, command=self.toggle_input, text="")
        self.storage_checkbox.grid(row=0, column=1, padx=0, pady=0)
        storage_label.grid(row=0, column=0, padx=10, pady=10)

        self.storage_input.grid_remove()
        store_button = ctk.CTkButton(scroll_frame, text="Speichern", command=self.save_settings)
        store_button.grid(row=1, column=0, sticky="w", pady=(15,0))

        self.load_settings()

    def toggle_input(self):
        if self.storage_check_var.get():
            self.show_input_field()
        else:
            self.hide_input_field()

    def show_input_field(self):
        self.storage_input.grid(row=0, column=2, padx=0, sticky="e")

    def hide_input_field(self):
        self.storage_input.grid_remove()

    def save_settings(self):
        if self.storage_check_var.get():
            storage_url = self.storage_input.get()
            self.controller.save_settings(storage_url)
        else:
            self.controller.settings.set_setting('api_url', None)
            self.storage_input.insert(0, "")
            self.controller.settings.save_settings()

        self.destroy()

    def load_settings(self):
        api_url = self.controller.settings.get_setting("api_url")

        if api_url:
            self.storage_input.insert(0, api_url)

        if self.storage_input.get():
            self.storage_check_var.set(True)
            self.toggle_input()







