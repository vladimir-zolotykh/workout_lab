#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import datetime
import tkinter as tk
from tkinter import ttk


class WorkoutEditor(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Workout Editor")
        self.geometry("600x400")

        # Workout timestamp
        ts_frame = ttk.Frame(self)
        ts_frame.grid(sticky=tk.W, padx=10, pady=5)
        ttk.Label(ts_frame, text="Started:").grid()
        self.timestamp_var = tk.StringVar()
        self.timestamp_var.set(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        ttk.Entry(ts_frame, textvariable=self.timestamp_var, state="readonly").grid()

        # scrolled = ScrolledFrame(self)
        # self.columnconfigure(0, weight=1)
        # scrolled.grid(sticky=tk.EW, padx=10, pady=5)
        # self.ex_frame = scrolled.scrolled_frame

        btn_frame = ttk.Frame(self)
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.grid(sticky=tk.EW, padx=10, pady=5)
        ttk.Button(btn_frame, text="Add Exercise").grid(sticky=tk.W)
        ttk.Button(btn_frame, text="Save Workout").grid(row=0, column=1)


if __name__ == "__main__":
    WorkoutEditor().mainloop()
