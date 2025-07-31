#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import io
import builtins
from typing import Iterator, Callable
from functools import wraps
import itertools
import tkinter as tk
import tkinter.simpledialog


def file_io_redirected(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        original_print = builtins.print
        with io.StringIO() as s:
            builtins.print = lambda *a, **k: original_print(*a, file=s, **k)
            try:
                method(self, *args, **kwargs)
            finally:
                builtins.print = original_print
            text = s.getvalue()
            ShowText(self.parent, text=text)

    return wrapper


def get_size(text: str) -> tuple[int, int]:
    it1: Iterator[str]
    it2: Iterator[str]
    it1, it2 = itertools.tee(text.split("\n"))
    return len(max(it1, key=len)), sum(1 for _ in it2)


class ShowText(tkinter.simpledialog.Dialog):
    def __init__(self, *args, text=None, **kwargs):
        self.text = text
        super().__init__(*args, **kwargs)

    def write(self, text: str) -> None:
        self.text_widget.insert(tk.INSERT, text)

    def body(self, master) -> tk.Widget:
        w, h = get_size(self.text)
        text = self.text_widget = tk.Text(master, width=w, height=h)
        text.grid()
        text.insert("1.0", self.text)
        return text
