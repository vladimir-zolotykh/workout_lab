#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk


class Workout(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Workout lab")
        self.geometry("404x603+360+164")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        box = tk.Frame(self)
        box.grid(column=0, row=0)
        tk.Button(box, text="add workout", command=self.add_workout).grid()
        tk.Button(box, text="OK").grid(sticky="w")

    def add_workout(self):
        pass


if __name__ == "__main__":
    Workout().mainloop()
