#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from sqlalchemy.orm import Session
import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog
import model as MD
import workout_editor as WE


class ShowAddDialog(tkinter.simpledialog.Dialog):
    def __init__(self, parent, session: Session, workout: MD.Workout, title=None):
        self.session = session
        self.workout = workout
        super().__init__(parent, title)

    def body(self, master) -> tk.Widget:
        exercise_names: list[str] = [
            e.name for e in self.session.query(MD.ExerciseName).all()
        ]
        workout_editor = WE.WorkoutEditor(
            master, self.session, exercise_names=exercise_names, workout=self.workout
        )
        workout_editor.grid(sticky=tk.NSEW)
        return workout_editor
