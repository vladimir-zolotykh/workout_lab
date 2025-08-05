#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from tkinter import ttk


class ScrolledFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        canvas = tk.Canvas(self)
        canvas.grid(column=0, row=0, sticky=tk.NSEW)
        self.scrolled_frame = tk.Frame(canvas)
        hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=canvas.xview)
        hbar.grid(column=0, row=1, sticky=tk.EW)
        vbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        vbar.grid(column=1, row=0, sticky=tk.NS)
        canvas.create_window((0, 0), window=self.scrolled_frame)
        self.scrolled_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox(tk.ALL))
        )
        canvas.configure(xscrollcommand=hbar.set)
        canvas.configure(yscrollcommand=vbar.set)
