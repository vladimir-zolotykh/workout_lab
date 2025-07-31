#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import itertools
import tkinter as tk
import tkinter.simpledialog


def get_size(text: str) -> tuple[int, int]:
    it1, it2 = itertools.tee(text.split("\n"))
    return len(max(it1, key=len)), sum(1 for _ in it2)


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
