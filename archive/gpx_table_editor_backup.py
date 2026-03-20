import tkinter as tk
from tkinter import ttk
from debug_decorator import log_all_methods


@log_all_methods

class GPXTableEditor(tk.Toplevel):

    def __init__(self, parent, document, update_callback, save_callback):

        super().__init__(parent)

        self.title("Track Table Editor")

        self.document = document

        self.segment = document.get_first_segment()

        self.tree = ttk.Treeview(
            self,
            columns=("lat", "lon"),
            show="headings"
        )

        self.tree.heading("lat", text="Latitude")
        self.tree.heading("lon", text="Longitude")

        self.tree.pack(fill="both", expand=True)

        if self.segment:

            for p in self.segment.points:

                self.tree.insert(
                    "",
                    "end",
                    values=(p.latitude, p.longitude)
                )