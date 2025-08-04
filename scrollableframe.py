#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        canvas = tk.Canvas(self)
        hbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=canvas.xview)
        vbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox(tk.ALL))
        )
        canvas.create_window((0, 0), window=self.scrollable_frame)
        canvas.configure(yscrollcommand=vbar.set)
        canvas.configure(xscrollcommand=hbar.set)
        canvas.grid(column=0, row=0, sticky=tk.NSEW)
        hbar.grid(column=0, row=1, sticky=tk.EW)
        vbar.grid(column=1, row=0, sticky=tk.NS)
