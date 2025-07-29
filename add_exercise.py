#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from tkinter import ttk


def on_ok():
    exercise = exercise_var.get()
    weight = weight_entry.get()
    reps = reps_entry.get()

    print(f"Exercise: {exercise}")
    print(f"Weight: {weight}")
    print(f"Reps: {reps}")

    root.destroy()


# --- Main window ---
root = tk.Tk()
root.title("Enter Exercise Data")

# --- Variables ---
exercise_var = tk.StringVar(value="squat")

# --- Widgets ---
tk.Label(root, text="Exercise:").grid(row=0, column=0, sticky="e")
exercise_menu = ttk.Combobox(
    root,
    textvariable=exercise_var,
    values=["squat", "deadlift", "pullup"],
    state="readonly",
)
exercise_menu.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Weight (kg):").grid(row=1, column=0, sticky="e")
weight_entry = tk.Entry(root)
weight_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Reps:").grid(row=2, column=0, sticky="e")
reps_entry = tk.Entry(root)
reps_entry.grid(row=2, column=1, padx=5, pady=5)

ok_button = tk.Button(root, text="OK", command=on_ok)
ok_button.grid(row=3, column=0, columnspan=2, pady=10)

# --- Start ---
root.mainloop()
