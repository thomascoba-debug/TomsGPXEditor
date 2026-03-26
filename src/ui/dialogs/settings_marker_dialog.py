import tkinter as tk
from tkinter import ttk
from src.ui.base import PersistentDialog

# Get logger for this module
import logging
logger = logging.getLogger(__name__)


class MarkerSettingsDialog(PersistentDialog):

    def __init__(self, parent, properties, save_callback):
        super().__init__(parent, properties, "MarkerSettingsDialog")
        
        self.save_callback = save_callback
        self.title("Marker Settings")

        # Store variables as class attributes
        self.marker_enabled = tk.BooleanVar(value=properties.get("marker_enabled", True))
        
        # Waypoints Einstellungen - 3 Farben + %
        self.waypoints_enabled = tk.BooleanVar(value=properties.get('dialogs.settings.rendering.waypoints.enabled', True))
        self.waypoints_percent = tk.IntVar(value=properties.get('dialogs.settings.rendering.waypoints.percent', 100))  # % statt Step
        self.waypoints_color_circle = tk.StringVar(value=properties.get('dialogs.settings.rendering.waypoints.color_circle', "#9B261E"))
        self.waypoints_color_outside = tk.StringVar(value=properties.get('dialogs.settings.rendering.waypoints.color_outside', "#C5542D"))
        self.waypoints_color_text = tk.StringVar(value=properties.get('dialogs.settings.rendering.waypoints.color_text', "#652A22"))
        
        # Track Points Einstellungen - 3 Farben + %
        self.trackpoints_enabled = tk.BooleanVar(value=properties.get('dialogs.settings.rendering.trackpoints.enabled', True))
        self.trackpoints_percent = tk.IntVar(value=properties.get('dialogs.settings.rendering.trackpoints.percent', 50))  # % statt Step
        self.trackpoints_color_circle = tk.StringVar(value=properties.get('dialogs.settings.rendering.trackpoints.color_circle', "#4169E1"))
        self.trackpoints_color_outside = tk.StringVar(value=properties.get('dialogs.settings.rendering.trackpoints.color_outside', "#6495ED"))
        self.trackpoints_color_text = tk.StringVar(value=properties.get('dialogs.settings.rendering.trackpoints.color_text', "#FFFFFF"))
        
        # Route Points Einstellungen - 3 Farben + %
        self.routepoints_enabled = tk.BooleanVar(value=properties.get('dialogs.settings.rendering.routepoints.enabled', True))
        self.routepoints_percent = tk.IntVar(value=properties.get('dialogs.settings.rendering.routepoints.percent', 50))  # % statt Step
        self.routepoints_color_circle = tk.StringVar(value=properties.get('dialogs.settings.rendering.routepoints.color_circle', "#228B22"))
        self.routepoints_color_outside = tk.StringVar(value=properties.get('dialogs.settings.rendering.routepoints.color_outside', "#32CD32"))
        self.routepoints_color_text = tk.StringVar(value=properties.get('dialogs.settings.rendering.routepoints.color_text', "#FFFFFF"))

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Master Switch
        top_frame = ttk.Frame(frame)
        top_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        master_cb = ttk.Checkbutton(
            top_frame,
            text="Marker Enabled",
            variable=self.marker_enabled,
            command=lambda: self._on_marker_enabled_change()
        )
        master_cb.grid(row=0, column=0, sticky="w")
        self._create_tooltip(master_cb, "Master-Schalter: Aktiviert/deaktiviert alle Marker auf der Karte")

        # Waypoints Sektion
        self._create_point_type_section(frame, "Waypoints", 1, 
                                       self.waypoints_enabled, self.waypoints_percent,
                                       self.waypoints_color_circle, self.waypoints_color_outside, self.waypoints_color_text)
        
        # Track Points Sektion
        self._create_point_type_section(frame, "Track Points", 2,
                                       self.trackpoints_enabled, self.trackpoints_percent,
                                       self.trackpoints_color_circle, self.trackpoints_color_outside, self.trackpoints_color_text)
        
        # Route Points Sektion
        self._create_point_type_section(frame, "Route Points", 3,
                                       self.routepoints_enabled, self.routepoints_percent,
                                       self.routepoints_color_circle, self.routepoints_color_outside, self.routepoints_color_text)

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=10)

        def ok():
            """Save settings and close dialog"""
            properties.set("marker_enabled", self.marker_enabled.get())
            
            # Waypoints
            properties.set('dialogs.settings.rendering.waypoints.enabled', self.waypoints_enabled.get())
            properties.set('dialogs.settings.rendering.waypoints.percent', self.waypoints_percent.get())  # % statt Step
            properties.set('dialogs.settings.rendering.waypoints.color_circle', self.waypoints_color_circle.get())
            properties.set('dialogs.settings.rendering.waypoints.color_outside', self.waypoints_color_outside.get())
            properties.set('dialogs.settings.rendering.waypoints.color_text', self.waypoints_color_text.get())
            
            # Track Points
            properties.set('dialogs.settings.rendering.trackpoints.enabled', self.trackpoints_enabled.get())
            properties.set('dialogs.settings.rendering.trackpoints.percent', self.trackpoints_percent.get())  # % statt Step
            properties.set('dialogs.settings.rendering.trackpoints.color_circle', self.trackpoints_color_circle.get())
            properties.set('dialogs.settings.rendering.trackpoints.color_outside', self.trackpoints_color_outside.get())
            properties.set('dialogs.settings.rendering.trackpoints.color_text', self.trackpoints_color_text.get())
            
            # Route Points
            properties.set('dialogs.settings.rendering.routepoints.enabled', self.routepoints_enabled.get())
            properties.set('dialogs.settings.rendering.routepoints.percent', self.routepoints_percent.get())  # % statt Step
            properties.set('dialogs.settings.rendering.routepoints.color_circle', self.routepoints_color_circle.get())
            properties.set('dialogs.settings.rendering.routepoints.color_outside', self.routepoints_color_outside.get())
            properties.set('dialogs.settings.rendering.routepoints.color_text', self.routepoints_color_text.get())
            
            save_callback()
            self._on_close()

        def cancel():
            """Close dialog without saving"""
            self._on_close()

        ttk.Button(btn_frame, text="OK", command=ok).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=cancel).pack(side="left", padx=5)
    
    def _create_point_type_section(self, parent, title, row, enabled_var, percent_var, color_circle_var, color_outside_var, color_text_var):
        """Erstellt eine Sektion für einen Punkt-Typ mit 3 Farben und %"""
        
        section_frame = ttk.LabelFrame(parent, text=title)
        section_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=5)
        section_frame.columnconfigure(1, weight=1)
        
        # Row 0: Enabled Checkbox mit Tooltip
        enabled_cb = ttk.Checkbutton(section_frame, text="Enabled", variable=enabled_var)
        enabled_cb.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self._create_tooltip(enabled_cb, "Aktiviert/deaktiviert die Anzeige dieses Punkt-Typs auf der Karte")
        
        # Row 1: % Label, Entry, Slider (engeres Layout)
        percent_label = ttk.Label(section_frame, text="Points:")
        percent_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self._create_tooltip(percent_label, "Prozentsatz der angezeigten Punkte")
        
        # % Entry für genaue Eingabe
        percent_entry = ttk.Entry(section_frame, textvariable=percent_var, width=8)
        percent_entry.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        self._create_tooltip(percent_entry, "Ganzzahliger Prozentsatz (1-100)")
        
        # Validierung für % Entry (nur ganze Zahlen 1-100)
        def validate_percent_input(*args):
            try:
                value = percent_var.get()
                if value < 1:
                    percent_var.set(1)
                elif value > 100:
                    percent_var.set(100)
            except:
                percent_var.set(50)
        
        percent_var.trace('w', validate_percent_input)
        
        # Key-Press Validierung für nur Zahlen
        def validate_percent_keypress(event):
            if event.char and not event.char.isdigit() and event.keysym not in ['BackSpace', 'Delete', 'Left', 'Right', 'Home', 'End']:
                return "break"
            return None
        
        percent_entry.bind('<Key>', validate_percent_keypress)
        
        # Slider mit % Anzeige (kürzer) - ganzzahlige Konvertierung
        percent_slider = ttk.Scale(section_frame, from_=1, to=100, orient=tk.HORIZONTAL, 
                                  variable=percent_var, length=120,
                                  command=lambda value: percent_var.set(int(float(value))))
        percent_slider.grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self._create_tooltip(percent_slider, "Visuelle Einstellung des Prozentsatzes")
        
        # % Label neben Slider
        percent_value_label = ttk.Label(section_frame, text="%")
        percent_value_label.grid(row=1, column=3, sticky="w", padx=2, pady=2)
        self._create_tooltip(percent_value_label, "Prozentsatz")
        
        # Row 2: Inner Circle Color + Preview mit Tooltip
        inner_circle_label = ttk.Label(section_frame, text="Inner Circle:")
        inner_circle_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self._create_tooltip(inner_circle_label, "Farbe des inneren Marker-Kreises")
        
        inner_circle_btn = tk.Button(section_frame, text="    ", bg=color_circle_var.get(), 
                                   command=lambda: self._pick_color(color_circle_var, inner_circle_btn))
        inner_circle_btn.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        self._create_tooltip(inner_circle_btn, "Farbauswahl für den inneren Kreis des Markers")
        
        # Row 3: Outside Circle Color mit Tooltip
        outside_circle_label = ttk.Label(section_frame, text="Outside Circle:")
        outside_circle_label.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self._create_tooltip(outside_circle_label, "Farbe des äußeren Marker-Kreises")
        
        outside_circle_btn = tk.Button(section_frame, text="    ", bg=color_outside_var.get(), 
                                     command=lambda: self._pick_color(color_outside_var, outside_circle_btn))
        outside_circle_btn.grid(row=3, column=1, sticky="w", padx=5, pady=2)
        self._create_tooltip(outside_circle_btn, "Farbauswahl für den äußeren Kreis des Markers")
        
        # Row 4: Text Color mit Tooltip
        text_color_label = ttk.Label(section_frame, text="Text Color:")
        text_color_label.grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self._create_tooltip(text_color_label, "Farbe des Markertextes")
        
        text_color_btn = tk.Button(section_frame, text="    ", bg=color_text_var.get(), 
                                 command=lambda: self._pick_color(color_text_var, text_color_btn))
        text_color_btn.grid(row=4, column=1, sticky="w", padx=5, pady=2)
        self._create_tooltip(text_color_btn, "Farbauswahl für den Markertext")
        
        # Row 2-4: Preview Canvas rechts von den Farbauswahlen mit Tooltip
        preview_canvas = tk.Canvas(section_frame, width=60, height=100, bg="white", 
                                 relief="flat", borderwidth=0, highlightthickness=0)
        preview_canvas.grid(row=2, column=2, rowspan=3, sticky="ns", padx=10, pady=2)
        self._create_tooltip(preview_canvas, "Live-Vorschau des Markers mit allen 3 Farben")
        
        # Update preview when colors change
        def update_preview():
            inner_circle_btn.configure(bg=color_circle_var.get())
            outside_circle_btn.configure(bg=color_outside_var.get())
            text_color_btn.configure(bg=color_text_var.get())
            self._draw_marker_preview(preview_canvas, color_circle_var.get(), color_outside_var.get(), color_text_var.get())
        
        color_circle_var.trace('w', lambda *args: update_preview())
        color_outside_var.trace('w', lambda *args: update_preview())
        color_text_var.trace('w', lambda *args: update_preview())
        
        # Initial preview
        update_preview()
    
    def _create_tooltip(self, widget, text):
        """Erstellt einen Tooltip für ein Widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, background="lightyellow", 
                           relief="solid", borderwidth=1, font=("TkDefaultFont", 9))
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def _pick_color(self, color_var, color_btn):
        """Öffne Farbauswahl-Dialog"""
        try:
            color = tk.colorchooser.askcolor(initialcolor=color_var.get())[1]
            if color:
                color_var.set(color)
                color_btn.configure(bg=color)
                self._update_preview()
            # Halte Dialog im Vordergrund
            self.lift()
        except Exception as e:
            logger.debug(f"Fehler bei Farbauswahl: {e}")

    def _draw_marker_preview(self, canvas, color_circle, color_outside, color_text):
        """Zeichnet Marker-Vorschau mit 3 Farben"""
        try:
            canvas.delete("all")
            
            # Marker zeichnen (vereinfacht)
            cx, cy = 30, 50  # Zentriert in der höheren Canvas
            radius = 15
            
            # Äußerer Kreis
            canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, 
                              fill=color_outside, outline="")
            
            # Innerer Kreis
            inner_radius = radius * 0.6
            canvas.create_oval(cx - inner_radius, cy - inner_radius, 
                              cx + inner_radius, cy + inner_radius, 
                              fill=color_circle, outline="")
            
            # Text (vereinfacht als Punkt)
            canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, 
                              fill=color_text, outline="")
            
        except Exception as e:
            logger.debug(f"Fehler bei Marker-Vorschau: {e}")

    def _update_preview(self):
        """Aktualisiere alle Vorschauen"""
        try:
            # Hier könnten alle Vorschauen aktualisiert werden
            pass
        except Exception as e:
            logger.debug(f"Fehler bei Vorschau-Update: {e}")

    def _on_marker_enabled_change(self):
        """Reagiere auf Änderung der Marker-Aktivierung"""
        try:
            # Hier könnte Logik für Master-Schalter implementiert werden
            pass
        except Exception as e:
            logger.debug(f"Fehler bei Marker-Aktivierung: {e}")

    def _on_close(self):
        """Speichere Geometrie und schließe Dialog"""
        logger.debug(f"MarkerSettingsDialog: Rufe super()._on_close() auf")
        super()._on_close()
        logger.debug(f"MarkerSettingsDialog: super()._on_close() abgeschlossen")
