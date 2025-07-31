#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
import tkinter.simpledialog


def get_size(text: str) -> tuple[int, int]:
    width: int = 0
    height: int = 0
    for line in text.split("\n"):
        if len(line) > width:
            width = len(line)
        height += 1
    return width, height


class ShowText(tkinter.simpledialog.Dialog):
    def __init__(self, *args, text=None, **kwargs):
        self.text = text
        super().__init__(*args, **kwargs)

    def body(self, master):
        w, h = get_size(self.text)
        text = tk.Text(master, width=w, height=h)
        text.grid()
        text.insert("1.0", self.text)
        return text
