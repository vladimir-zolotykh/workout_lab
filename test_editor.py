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

        ts_frame = ttk.Frame(self)
        ts_frame.grid(row=0, sticky=tk.W, padx=10, pady=5)
        ttk.Label(ts_frame, text="Started:").grid()
        self.timestamp_var = tk.StringVar()
        self.timestamp_var.set(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        ttk.Entry(ts_frame, textvariable=self.timestamp_var, state="readonly").grid()

        canv = tk.Canvas(self, width=500, height=200)
        canv.grid(row=1, sticky=tk.NSEW)
        canv.create_line(0, 0, 500, 200)
        canv.create_line(0, 200, 500, 0)
        self.rowconfigure(1, weight=1)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, columnspan=2, sticky=tk.EW, padx=10, pady=5)

        btn_frame.columnconfigure(0, weight=1)
        ttk.Button(btn_frame, text="Add Exercise").grid(row=0, column=0, sticky=tk.W)
        ttk.Button(btn_frame, text="Save Workout").grid(row=0, column=1, sticky=tk.E)


if __name__ == "__main__":
    WorkoutEditor().mainloop()
