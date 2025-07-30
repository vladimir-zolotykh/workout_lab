#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
import tkinter.simpledialog


class ShowText(tkinter.simpledialog.Dialog):
    def __init__(self, *args, text=None, **kwargs):
        self.text = text
        super().__init__(*args, **kwargs)

    def body(self, master):
        text = tk.Text(master, width=50, height=10)
        text.grid()
        text.insert("1.0", self.text)
        return text
