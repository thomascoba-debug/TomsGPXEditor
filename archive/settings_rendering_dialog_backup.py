import tkinter as tk
from tkinter import ttk
from dialog_base import PersistentDialog
from debug_decorator import log_all_methods


@log_all_methods

class RenderingSettingsDialog(PersistentDialog):

    def __init__(self, parent, properties, save_callback):

        super().__init__(parent, properties)

        self.title("Rendering Settings")

        self.properties = properties
        self.save_callback = save_callback

        zoom_scaling_enabled = tk.BooleanVar(
            value=properties.get("zoom_scaling_enabled", True)
        )

        downsample_step = tk.IntVar(
            value=properties.get("downsample_step", 1)
        )

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Checkbutton(
            frame,
            text="Zoom Scaling Enabled",
            variable=zoom_scaling_enabled
        ).grid(row=0, column=0, sticky="w", pady=5)

        ttk.Label(frame, text="Downsample Step").grid(row=1, column=0, sticky="w")

        ttk.Entry(
            frame,
            textvariable=downsample_step,
            width=10
        ).grid(row=1, column=1, sticky="w")

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)

        ttk.Button(
            button_frame,
            text="Close",
            command=self._on_close
        ).pack(side="left", padx=5)

        def ok():

            properties.set(
                "zoom_scaling_enabled",
                zoom_scaling_enabled.get()
            )

            properties.set(
                "downsample_step",
                downsample_step.get()
            )

            properties.save()

            if save_callback:
                save_callback()

            self._on_close()

        ttk.Button(
            button_frame,
            text="OK",
            command=ok
        ).pack(side="left")