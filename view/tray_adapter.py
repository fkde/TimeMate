import os
import sys
from PIL import Image
from threading import Thread

try:
    import gi
    gi.require_version('AppIndicator3', '0.1')
    gi.require_version('Gtk', '3.0')
    from gi.repository import AppIndicator3, Gtk
    BACKEND = "appindicator"
except Exception:
    BACKEND = None

if BACKEND is None:
    try:
        import pystray
        from PIL import Image
        from pystray import MenuItem as item
        BACKEND = "pystray"
    except ImportError:
        BACKEND = None

class TrayIcon:
    def __init__(self, controller):
        self.controller = controller
        self.icon_path_green = os.path.join(sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.getcwd(), "icons/timemate-green.png")
        self.icon_path_red = os.path.join(sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.getcwd(), "icons/timemate-red.png")
        self.current_icon_path = self.icon_path_red

        if BACKEND == "appindicator":
            self.indicator = AppIndicator3.Indicator.new(
                "TimeMate", self.current_icon_path, AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self._build_menu_appindicator()
            Thread(target=Gtk.main, daemon=True).start()

        elif BACKEND == "pystray":
            image = Image.open(self.current_icon_path)
            self.tray = pystray.Icon("TimeMate", image, "TimeMate", menu=pystray.Menu(
                item("Öffnen", lambda _: self.controller.show_window()),
                item("Beenden", lambda _: self.controller.quit())
            ))
            Thread(target=self.tray.run, daemon=True).start()

        else:
            print("⚠️ Kein passendes Tray-System gefunden. Fallback aktiv.")

    def _build_menu(self):
        menu = Gtk.Menu()

        item_show = Gtk.MenuItem(label="Öffnen")
        item_show.connect("activate", lambda _: self.controller.show_window())
        menu.append(item_show)

        item_quit = Gtk.MenuItem(label="Beenden")
        item_quit.connect("activate", lambda _: self.controller.quit())
        menu.append(item_quit)

        menu.show_all()
        self.indicator.set_menu(menu)

    def _build_menu_appindicator(self):
        menu = Gtk.Menu()

        item_show = Gtk.MenuItem(label="Öffnen")
        item_show.connect("activate", lambda _: self.controller.show_window())
        menu.append(item_show)

        item_quit = Gtk.MenuItem(label="Beenden")
        item_quit.connect("activate", lambda _: self.controller.quit())
        menu.append(item_quit)

        menu.show_all()
        self.indicator.set_menu(menu)

    def set_running(self, running):
        self.current_icon_path = self.icon_path_green if running else self.icon_path_red

        if BACKEND == "appindicator":
            self.indicator.set_icon(self.current_icon_path)
        elif BACKEND == "pystray" and hasattr(self, "tray"):
            self.tray.icon = Image.open(self.current_icon_path)