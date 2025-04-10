Die README im Markdown-Format ist nun fertig und kann direkt in die `README.md` eingefügt werden. Hier ist der vollständige Inhalt:

```markdown
# TimeMate – Arbeitszeiterfassung

**TimeMate** ist eine einfach zu bedienende Arbeitszeiterfassungs-App für Windows, Linux und macOS, die mit einer benutzerfreundlichen Oberfläche und einem Tray-Icon arbeitet. 

## 📦 Voraussetzungen

- Python 3.6 oder höher
- Pip (Python-Paket-Manager)
- CustomTkinter
- pystray / AppIndicator3 (für Tray-Icons)

### Installation

1. **Clone das Repository**:

   ```bash
   git clone <repository-url>
   cd py-timer
   ```

2. **Erstelle ein virtuelles Umfeld und installiere die Abhängigkeiten**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Für Linux/macOS
   .\.venv\Scripts\activate   # Für Windows
   pip install -r requirements.txt
   ```

3. **Installiere erforderliche zusätzliche Pakete** (falls noch nicht installiert):

   ```bash
   pip install pystray pillow
   ```

4. **Optional: System-abhängige Abhängigkeiten für AppIndicator3 (Linux)**:

   ```bash
   sudo apt install libayatana-appindicator3-dev
   ```

5. **Setze die App-Icons und Assets**:

   - Lege die Icons in den Ordner `icons` ab (einschließlich `icon-green.png` und `icon-red.png` für das Tray-Icon).
   - (Optional) Füge eine `.ico`-Datei für Windows hinzu (z. B. `timemate-green.ico`).

---

## 🚀 Benutzung

1. **Starten der Anwendung**:

   ```bash
   python main.py
   ```

2. **Funktionen der Benutzeroberfläche**:

   - **Timer starten**: Klick auf den "Start"-Button
   - **Timer anhalten**: Klick auf "Pause"
   - **Timer zurücksetzen**: Klick auf "Abbrechen"
   - **Zeiterfassung buchen**: Füge Titel und Beschreibung hinzu und klicke auf "Buchen"
   - **Zeiterfassungen anzeigen**: Über das Menü "Ansicht > Zeiterfassungen" kannst du alle gespeicherten Zeiterfassungen sehen.
   
3. **Tray-Icon**:  
   Die Anwendung hat ein Tray-Icon, das den aktuellen Zustand des Timers anzeigt:
   - Grüner Punkt (Timer läuft)
   - Roter Punkt (Timer pausiert)

4. **Zeiterfassungslog**:  
   Das Log wird in einer Scrollable-Ansicht angezeigt, die sich mit dem Mausrad durchscrollen lässt. Es zeigt alle gespeicherten Einträge mit Start-/Endzeit, Dauer und Beschreibung an.

---

## 🛠️ Funktionen

- **Starten / Stoppen / Zurücksetzen des Timers**
- **Speichern der Zeiterfassungen**: Bucht den Zeitraum mit Titel und optionaler Beschreibung.
- **Zeiterfassungs-Log anzeigen**: Zeigt alle vorherigen Zeiterfassungen in einem scrollbaren Fenster an.
- **Menüleiste**: Menü mit Optionen wie „Zeiterfassungen anzeigen“ und „Beenden“.

---

## 🔧 Entwickler-Setup

Für lokale Änderungen am Code:

1. **Erstelle ein virtuelles Umfeld**:

   ```bash
   python3 -m venv .venv
   ```

2. **Installiere die Abhängigkeiten**:

   ```bash
   pip install -r requirements.txt
   ```

---

## 💡 Hinweise zur Tray-Integration

- **Linux (Wayland)**: Wir verwenden pystray und AppIndicator3 für das Tray-Icon. Auf Wayland-Systemen müssen spezifische Abhängigkeiten installiert werden:
  
  ```bash
  sudo apt install libayatana-appindicator3-dev
  ```

- **Windows**: Das Tray-Icon funktioniert mit pystray. Es wird ein grünes oder rotes Icon angezeigt, je nachdem, ob der Timer läuft.

---

## 📝 To-Do / Erweiterungen

- **Exportfunktion für Log**: Möglichkeit, die Zeiterfassungen als CSV oder HTML zu exportieren.
- **Farbliche Anpassung**: Der Button-Stil und das Tray-Icon können weiter angepasst werden, um verschiedene Zustände anzuzeigen.

---

## 🏗️ Weitere Anpassungen und Erweiterungen

- **Farbänderungen für Buttons**: Beispielweise können Start, Stop und Reset verschiedene Farben haben, um das Benutzererlebnis zu verbessern.
- **Benachrichtigungen**: Popup-Benachrichtigungen könnten bei Timerstart und -stopp hinzugefügt werden.

---

## 🖥️ Troubleshooting

1. **Fehlendes Tray-Icon**:  
   Wenn das Tray-Icon nicht angezeigt wird, stelle sicher, dass du alle Abhängigkeiten für AppIndicator3 auf Linux installiert hast und dass `pystray` korrekt verwendet wird.

2. **Scrollbar nicht funktionierend**:  
   Falls das Scrollen im Log-Fenster nicht funktioniert, stelle sicher, dass du das `MouseWheel`-Event korrekt an den Scroll-Frame bindest.

3. **Fehlende Zeitformatierung**:  
   Überprüfe, ob der `seconds` Wert korrekt als Ganzzahl übergeben wird, bevor er in `timedelta` verwendet wird.

---

### Viel Spaß beim Benutzen! 🎉
Für weitere Fragen oder Feature-Anfragen stehe ich jederzeit zur Verfügung! 😊
```