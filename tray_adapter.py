import os
import sys
import threading
from session_manager import SessionManager

# Optional imports (je nach Umgebung)
try:
    from pystray import Icon as PystrayIcon, MenuItem as item, Menu
    from PIL import Image, ImageDraw
    HAVE_PYSTRAY = True
except ImportError:
    HAVE_PYSTRAY = False

try:
    import gi
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3, Gtk
    HAVE_APPINDICATOR = True
except ImportError:
    HAVE_APPINDICATOR = False

def resource_path(relative_path):
    """Ermittle Pfad zu Ressourcen, auch wenn gepackt (PyInstaller)"""
    try:
        # Wenn gepackt mit PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Wenn normal ausgeführt
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ICON_PATH = os.path.join(os.path.dirname(__file__), "icons")

class TrayAdapter:
    def __init__(self):
        self.session = SessionManager()
        self.gui_reference = None
        self.indicator = None
        self.icon_state = "stopped"
        self.backend = None

        print("XDG_CURRENT_DESKTOP:", os.environ.get("XDG_CURRENT_DESKTOP"))
        print("XDG_SESSION_TYPE:", os.environ.get("XDG_SESSION_TYPE"))

        if os.environ.get("XDG_SESSION_TYPE") == "x11" and HAVE_PYSTRAY:
            self.backend = "pystray"
        elif os.environ.get("XDG_SESSION_TYPE") == "wayland" and HAVE_APPINDICATOR:
            self.backend = "appindicator"

    def register_gui(self, gui):
        self.gui_reference = gui

    def get_session_state(self):
        return self.session.get_state()

    def update_gui(self):
        if self.gui_reference:
            self.gui_reference.update_from_session()

    def start_timer(self, *_):
        self.session.start()
        self.set_icon_by_state("running")
        self.update_gui()

    def pause_timer(self, *_):
        self.session.pause()
        self.set_icon_by_state("paused")
        self.update_gui()

    def reset_timer(self):
        self.session.reset()
        self.set_icon_by_state("stopped")
        self.update_gui()

    def book_session(self, text="", description=""):
        self.session.book(text, description)
        self.set_icon_by_state("stopped")
        self.update_gui()

    def show_gui(self, *_):
        if self.gui_reference:
            self.gui_reference.deiconify()
            self.gui_reference.focus()

    def quit_app(self, *_):
        if self.backend == "appindicator":
            Gtk.main_quit()
        elif self.gui_reference:
            self.gui_reference.destroy()

    def run(self):
        if self.backend == "pystray":
            self.run_pystray()
        elif self.backend == "appindicator":
            self.run_appindicator()
        else:
            print("Kein passendes Tray-System gefunden. Fallback aktiv.")

    def set_icon(self, name):
        self.indicator.set_icon_full(name, "TimeMate")

    def set_icon_by_state(self, state):
        if self.backend == "appindicator":
            icon_file = "timemate-green.png" if state == "running" else "timemate-red.png"
            full_path = resource_path("icons/" + icon_file)
            self.indicator.set_icon_full(full_path, "TimeMate")

    # --- Backend: pystray (X11) ---
    def run_pystray(self):
        image = Image.new("RGB", (64, 64), (30, 30, 30))
        draw = ImageDraw.Draw(image)
        draw.ellipse((16, 16, 48, 48), fill=(0, 122, 255))

        menu = Menu(
            item("Start", self.start_timer),
            item("Stop", self.pause_timer),
            item("Buchen", self.book_session),
            item("Fenster öffnen", self.show_gui),
            item("Beenden", self.quit_app)
        )

        icon = PystrayIcon("TimeMate", image, "TimeMate", menu)
        threading.Thread(target=icon.run, daemon=True).start()

    # --- Backend: AppIndicator (Wayland / GNOME) ---
    def run_appindicator(self):
        self.indicator = AppIndicator3.Indicator.new(
            "TimeMate", "media-playback-start", AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        menu = Gtk.Menu()

        def make_menu_item(label, callback):
            item = Gtk.MenuItem(label=label)
            item.connect("activate", callback)
            item.show()
            return item

        def make_menu_divider():
            item = Gtk.MenuItem(label="---")
            item.show()
            return item

        def on_icon_click(indicator, button):
            print("🖱️ Icon wurde angeklickt")
            self.show_gui()

        menu.append(make_menu_item("Start", self.start_timer))
        menu.append(make_menu_item("Pause", self.pause_timer))
        menu.append(make_menu_divider())
        menu.append(make_menu_item("Fenster öffnen", self.show_gui))
        menu.append(make_menu_item("Beenden", self.quit_app))

        self.indicator.set_menu(menu)
        self.set_icon_by_state("stopped")

        threading.Thread(target=Gtk.main, daemon=True).start()
