import tkinter as tk
from tkinter import ttk
import logging
from src.ui.base import PersistentDialog

# Get logger for this module
logger = logging.getLogger(__name__)


class PropertiesEditorDialog(PersistentDialog):

    def __init__(self, parent, properties, save_callback, modal=False):
        logger.debug(f"__init__ START: parent={type(parent).__name__}, properties keys={list(properties.data.keys())}, save_callback={save_callback.__name__ if hasattr(save_callback, '__name__') else type(save_callback)}")
        super().__init__(parent, properties, "PropertiesEditorDialog", modal=modal)
        self.save_callback = save_callback
        self.title("Properties Editor")
        logger.debug(f"Dialog title gesetzt")
        
        # Speichere Original-Typen für spätere Rekonstruktion
        self.original_types = {}
        # Speichere Original-Daten für Undo-Funktion
        self.original_data = dict(properties.data)  # Deep copy
        logger.debug(f"original_types dict initialisiert")
        logger.debug(f"original_data gespeichert: {len(self.original_data)} Keys")

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        logger.debug(f"Frame erstellt und konfiguriert")

        # Treeview mit Scrollbars
        tree_container = ttk.Frame(frame)
        tree_container.grid(row=0, column=0, sticky="nsew", columnspan=4)
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_container, columns=("value",), show="tree", height=15)
        self.tree.heading("#0", text="Key")  # Tree column shows key
        self.tree.heading("value", text="Value")
        self.tree.column("#0", width=250, minwidth=100)  # Tree column for keys
        self.tree.column("value", width=350, minwidth=100)  # Value column
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        logger.debug(f"Treeview erstellt mit 2 Spalten (key, value), height=15")

        # Treeview mit ALLEN Properties füllen (extrem einfache Version)
        count = 0
        
        def add_simple_items(parent, data, prefix="", depth=0):
            """Einfache Funktion ohne jegliche Komplexität"""
            nonlocal count
            if depth > 5:  # Tiefe-Limit
                return
            
            for key, value in data.items():
                # Speichere Original-Typ nur für Top-Level
                if not prefix:
                    self.original_types[key] = type(value)
                
                # Einfache Wert-Anzeige
                if isinstance(value, dict):
                    display_value = f"{{dict}} {len(value)} items"
                    item = self.tree.insert(parent, "end", text=f"{prefix}{key}", values=(display_value,), open=True)
                    # Tiefer gehen für alle Dicts mit Tiefe-Limit
                    if depth < 4 and len(value) > 0:
                        add_simple_items(item, value, f"{prefix}{key}.", depth + 1)
                elif isinstance(value, list):
                    display_value = f"[list] {len(value)} items"
                    self.tree.insert(parent, "end", text=f"{prefix}{key}", values=(display_value,))
                else:
                    display_value = str(value)[:100]
                    self.tree.insert(parent, "end", text=f"{prefix}{key}", values=(display_value,))
                count += 1
        
        try:
            add_simple_items("", properties.data)
        except Exception as e:
            # Fallback: Zeige nur Top-Level
            for key, value in properties.data.items():
                self.original_types[key] = type(value)
                if isinstance(value, dict):
                    display_value = f"{{dict}} {len(value)} items"
                elif isinstance(value, list):
                    display_value = f"[list] {len(value)} items"
                else:
                    display_value = str(value)[:100]
                self.tree.insert("", "end", text=key, values=(display_value,))
                count += 1

        self.tree.bind('<Double-1>', self._on_double_click)
        logger.debug(f"Double-Click Event für Treeview gebunden")

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=10)
        btn_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)
        logger.debug(f"Button-Frame erstellt")

        ttk.Button(btn_frame, text="Add", command=self._add_entry).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self._delete_entry).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self._refresh_tree).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="OK", command=self._save).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self._close_without_saving).grid(row=0, column=4, padx=5)
        logger.debug(f"5 Buttons erstellt und platziert")
        
        logger.debug(f"__init__ ENDE")

    def _on_double_click(self, event):
        logger.debug(f"_on_double_click START: event.x={event.x}, event.y={event.y}")
        # Zelle editieren
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        logger.debug(f"Identifizierte item='{item}', column='{column}'")
        
        if not item or column not in ('#1', '#2'):
            logger.debug(f"_on_double_click ABBRUCH: item={item}, column={column}")
            return
        
        x, y, width, height = self.tree.bbox(item, column)
        logger.debug(f"bbox: x={x}, y={y}, width={width}, height={height}")
        
        value = self.tree.set(item, column)
        logger.debug(f"Aktueller Wert: '{value}'")
        
        entry = tk.Entry(self.tree)
        entry.insert(0, value)
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus()
        logger.debug(f"Entry-Widget erstellt und platziert, fokussiert")

        def on_focus_out(event):
            logger.debug(f"on_focus_out START")
            new_value = entry.get()
            logger.debug(f"Neuer Wert aus Entry: '{new_value}'")
            
            col = self.tree.heading(column)['text'].lower()
            values = list(self.tree.item(item, 'values'))
            logger.debug(f"Aktuelle values: {values}, column_name: '{col}'")
            
            idx = 0 if column == '#1' else 1
            logger.debug(f"Setze index {idx} auf '{new_value}'")
            
            values[idx] = new_value
            self.tree.item(item, values=values)
            logger.debug(f"Treeview-Item aktualisiert: {values}")
            
            entry.destroy()
            logger.debug(f"Entry-Widget zerstört")
            logger.debug(f"on_focus_out ENDE")
            
        entry.bind('<FocusOut>', on_focus_out)
        entry.bind('<Return>', lambda e: entry.event_generate('<FocusOut>'))
        logger.debug(f"FocusOut und Return Events gebunden")
        logger.debug(f"_on_double_click ENDE")

    def _add_entry(self):
        logger.debug(f"_add_entry START")
        # Fügt ein neues Key/Value-Paar hinzu
        def add():
            logger.debug(f"add() START")
            key = key_var.get().strip()
            value = value_var.get().strip()
            type_selection = type_var.get()
            logger.debug(f"Neue Entry-Werte: key='{key}', value='{value}', type='{type_selection}'")
            
            if key:
                # Konvertiere Wert basierend auf Typ-Auswahl
                try:
                    if type_selection == "bool":
                        processed_value = value.lower() in ('true', '1', 'yes')
                    elif type_selection == "int":
                        processed_value = int(value) if value else 0
                    elif type_selection == "float":
                        processed_value = float(value) if value else 0.0
                    elif type_selection == "list":
                        processed_value = value.split(',') if value else []
                    elif type_selection == "dict":
                        # Einfache key:value Paare parsen
                        processed_value = {}
                        if value:
                            try:
                                pairs = value.split(',')
                                for pair in pairs:
                                    if ':' in pair:
                                        k, v = pair.split(':', 1)
                                        processed_value[k.strip()] = v.strip()
                            except:
                                pass
                    else:  # string
                        processed_value = value
                    
                    self.tree.insert('', 'end', values=(key, str(processed_value)))
                    logger.debug(f"Treeview-Row eingefügt: ('{key}', '{processed_value}')")
                    self.original_types[key] = {'bool': bool, 'int': int, 'float': float, 'list': list, 'dict': dict, 'string': str}[type_selection]
                    logger.debug(f"Original-Typ für '{key}' gespeichert: {type_selection}")
                except Exception as e:
                    logger.debug(f"Fehler bei der Konvertierung: {e}")
                    self.tree.insert('', 'end', values=(key, value))
                    self.original_types[key] = str
                    logger.debug(f"Als String gespeichert aufgrund von Fehler: {key}")
            else:
                logger.debug(f"add() ABBRUCH: key ist leer")
            
            logger.debug(f"Schließe Toplevel-Dialog")
            top.destroy()
            logger.debug(f"add() ENDE")

        top = tk.Toplevel(self)
        top.title('Add New Property')
        logger.debug(f"Toplevel-Dialog erstellt")
        
        # Key input
        tk.Label(top, text='Key:').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        key_var = tk.StringVar()
        tk.Entry(top, textvariable=key_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        logger.debug(f"Key-Label und Entry erstellt")
        
        # Value input
        tk.Label(top, text='Value:').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        value_var = tk.StringVar()
        tk.Entry(top, textvariable=value_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        logger.debug(f"Value-Label und Entry erstellt")
        
        # Type selection
        tk.Label(top, text='Type:').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        type_var = tk.StringVar(value="string")
        type_combo = ttk.Combobox(top, textvariable=type_var, 
                                   values=["string", "int", "float", "bool", "list", "dict"], 
                                   state="readonly", width=28)
        type_combo.grid(row=2, column=1, padx=5, pady=5)
        logger.debug(f"Type-Auswahl erstellt")
        
        # Buttons
        btn_frame = ttk.Frame(top)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text='Add', command=add).pack(side="left", padx=5)
        ttk.Button(btn_frame, text='Cancel', command=top.destroy).pack(side="left", padx=5)
        logger.debug(f"Buttons erstellt")
        
        top.grab_set()
        logger.debug(f"Toplevel-Dialog modal gesetzt")
        logger.debug(f"_add_entry ENDE")

    def _delete_entry(self):
        logger.debug(f"_delete_entry START")
        # Löscht das selektierte Key/Value-Paar
        selected = self.tree.selection()
        logger.debug(f"Selektierte Items: {selected}")
        
        for item in selected:
            values = self.tree.item(item)["values"]
            logger.debug(f"Lösche Item '{item}' mit Werten: {values}")
            self.tree.delete(item)
            logger.debug(f"Item '{item}' gelöscht")
        
        logger.debug(f"_delete_entry ENDE: {len(selected)} Items gelöscht")

    def _refresh_tree(self):
        logger.debug(f"_refresh_tree START")
        # Treeview leeren und neu laden
        for item in self.tree.get_children():
            self.tree.delete(item)
        logger.debug(f"Treeview geleert")
        
        # Treeview mit ALLEN Properties füllen (keine Ausnahmen mehr)
        logger.debug(f"Starte Treeview-Refresh mit properties.data: {self.properties.data}")
        count = 0
        for key, value in self.properties.data.items():
            # Speichere Original-Typ
            self.original_types[key] = type(value)
            logger.debug(f"Füge Property hinzu: key='{key}', value={repr(value)[:100]}, type={type(value).__name__}")
            
            # Format value für Anzeige
            if isinstance(value, dict):
                display_value = f"{{dict}} {len(value)} items"
            elif isinstance(value, list):
                display_value = f"[list] {len(value)} items"
            else:
                display_value = str(value)
            
            self.tree.insert("", "end", values=(key, display_value))
            count += 1
        logger.debug(f"Treeview-Refresh abgeschlossen: {count} Properties eingefügt")
        logger.debug(f"_refresh_tree ENDE")

    def _save(self):
        logger.debug(f"_save START")
        # Properties aus Treeview übernehmen
        new_data = {}
        logger.debug(f"Erstelle neue properties mit {len(self.tree.get_children())} Items")
        
        # Alle Treeview-Werte übernehmen und versuchen, in Original-Typ zurückzukonvertieren
        tree_items = self.tree.get_children()
        logger.debug(f"Verarbeite {len(tree_items)} Items aus Treeview")
        
        for item in tree_items:
            key, value_str = self.tree.item(item)["values"]
            logger.debug(f"Verarbeite Item: key='{key}', value_str='{value_str}'")
            
            # Versuche, in Original-Typ zurückzukonvertieren
            if key in self.original_types:
                orig_type = self.original_types[key]
                logger.debug(f"Original-Typ für '{key}': {orig_type.__name__}")
                
                # Für komplexe Typen (dict, list) behalte die Originaldaten aus properties.data
                if orig_type == dict or orig_type == list:
                    if key in self.properties.data and isinstance(self.properties.data[key], orig_type):
                        value = self.properties.data[key]
                        logger.debug(f"Behalte Original-{orig_type.__name__}: {repr(value)[:100]}")
                    else:
                        # Fallback: Versuche, aus dem String zu rekonstruieren
                        try:
                            if orig_type == list:
                                value = eval(value_str) if value_str.startswith('[') else []
                            else:  # dict
                                value = eval(value_str) if value_str.startswith('{') else {}
                            logger.debug(f"Rekonstruiert {orig_type.__name__}: {repr(value)[:100]}")
                        except Exception as e:
                            # Letzter Fallback: leere Struktur
                            value = [] if orig_type == list else {}
                            logger.debug(f"Konnte nicht rekonstruieren, nutze leeres {orig_type.__name__}: {value}")
                else:
                    # Für einfache Typen konvertiere den String
                    try:
                        if orig_type == bool:
                            value = value_str.lower() in ('true', '1', 'yes')
                        elif orig_type == int:
                            value = int(value_str) if value_str else 0
                        elif orig_type == float:
                            value = float(value_str) if value_str else 0.0
                        else:
                            value = value_str
                        logger.debug(f"Konvertiert zu {orig_type.__name__}: {value}")
                    except Exception as e:
                        value = value_str
                        logger.debug(f"Konvertierung fehlgeschlagen ({type(e).__name__}: {e}), behalte als string: {value}")
            else:
                # Neuer Eintrag, standardmäßig als string
                value = value_str
                logger.debug(f"Neuer Eintrag, behalte als string: {value}")
            
            new_data[key] = value
            logger.debug(f"new_data['{key}'] = {repr(value)}")
        
        # Behalte komplexe Properties aus Originaldaten, falls nicht im Treeview
        for key, value in self.properties.data.items():
            if key not in new_data:
                new_data[key] = value
                logger.debug(f"Behalte Original-Property '{key}': {repr(value)[:100]}")
        
        self.properties.data = new_data
        logger.debug(f"properties.data aktualisiert mit {len(new_data)} Keys")
        
        # Speichere Geometrie vor dem Schließen
        self._save_geometry()
        
        self.save_callback()
        logger.debug(f"save_callback() aufgerufen")
        
        self.destroy()
        logger.debug(f"Dialog zerstört")
        logger.debug(f"_save ENDE")

    def _close_without_saving(self):
        logger.debug(f"_close_without_saving START")
        # Original-Daten wiederherstellen
        self.properties.data = dict(self.original_data)  # Deep copy
        logger.debug(f"Original-Daten wiederhergestellt: {len(self.properties.data)} Keys")
        
        # Speichere Geometrie vor dem Schließen
        self._save_geometry()
        
        self.destroy()
        logger.debug(f"Dialog zerstört ohne zu speichern")
        logger.debug(f"_close_without_saving ENDE")

    def _on_close(self):
        logger.debug(f"_on_close START")
        # Speichere Properties und schließe Dialog
        logger.debug(f"PropertiesEditorDialog: Rufe super()._on_close() auf")
        super()._on_close()
        logger.debug(f"PropertiesEditorDialog: super()._on_close() abgeschlossen")
        logger.debug(f"_on_close ENDE")


