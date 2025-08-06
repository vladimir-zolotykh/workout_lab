#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from sqlalchemy import (
    Engine,
    create_engine,
)
import model as MD

# from scrollableframe import ScrollableFrame
from scrolledframe import ScrolledFrame


class WorkoutEditor(tk.Toplevel):
    def __init__(self, parent, session, exercise_names, workout=None):
        self.parent = parent
        super().__init__(parent)
        self.session = session
        self.exercise_names = exercise_names  # list[str]
        self.workout = workout
        self.exercise_widgets = []

        self.title("Workout Editor")
        self.geometry("600x400")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Workout timestamp
        ts_frame = ttk.Frame(self)
        ts_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(ts_frame, text="Started:").pack(side="left")
        self.timestamp_var = tk.StringVar()
        self.timestamp_var.set(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        ttk.Entry(ts_frame, textvariable=self.timestamp_var, state="readonly").pack(
            side="left"
        )

        # Scrolled Frame for exercises
        # self.ex_frame = ttk.Frame(self)
        # scrolled = ScrollableFrame(self)
        scrolled = ScrolledFrame(self)
        scrolled.pack(fill="both", expand=True, padx=10, pady=5)
        self.ex_frame = scrolled.scrolled_frame
        # self.ex_frame.pack(fill="both", expand=True, padx=10)

        # Add / Save buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Add Exercise", command=self.add_exercise).pack(
            side="left"
        )
        ttk.Button(btn_frame, text="Save Workout", command=self.save_workout).pack(
            side="right"
        )

        # Populate if editing an existing workout
        if self.workout:
            for ex in self.workout.exercises:
                self.add_exercise(exercise=ex)
        else:
            self.add_exercise()

    def on_close(self):
        if isinstance(self.parent, tk.Tk):
            self.parent.destroy()

    def add_exercise(self, exercise=None):
        frame = ttk.Frame(self.ex_frame)
        frame.pack(fill="x", pady=2)

        name_var = tk.StringVar(value=exercise.exercise_name.name if exercise else "")
        weight_var = tk.DoubleVar(value=exercise.weight if exercise else 0.0)
        reps_var = tk.IntVar(value=exercise.reps if exercise else 1)

        cb = ttk.Combobox(
            frame,
            textvariable=name_var,
            values=self.exercise_names,
            state="readonly",
            width=20,
        )
        cb.pack(side="left", padx=5)

        weight_entry = ttk.Entry(frame, textvariable=weight_var, width=7)
        weight_entry.pack(side="left", padx=5)
        reps_entry = ttk.Entry(frame, textvariable=reps_var, width=5)
        reps_entry.pack(side="left", padx=5)

        del_btn = ttk.Button(
            frame, text="Delete", command=lambda: self.remove_exercise(frame)
        )
        del_btn.pack(side="left", padx=5)

        self.exercise_widgets.append((frame, name_var, weight_var, reps_var))

    def remove_exercise(self, frame):
        for tup in self.exercise_widgets:
            if tup[0] == frame:
                self.exercise_widgets.remove(tup)
                break
        frame.destroy()

    def save_workout(self):
        # This method should create or update SQLAlchemy objects
        print("Saving workout:")
        started = datetime.strptime(self.timestamp_var.get(), "%Y-%m-%d %H:%M:%S")

        if not self.workout:
            from model import Workout  # adjust to your module

            self.workout = Workout(started=started)
            self.session.add(self.workout)
        else:
            self.workout.exercises.clear()  # reset if editing

        for _, name_var, weight_var, reps_var in self.exercise_widgets:
            ex_name = name_var.get()
            weight = weight_var.get()
            reps = reps_var.get()

            ex_name_obj = (
                self.session.query(MD.ExerciseName).filter_by(name=ex_name).first()
            )
            if not ex_name_obj:
                continue  # or create?

            from model import Exercise  # adjust

            exercise = Exercise(
                exercise_name=ex_name_obj,
                weight=weight,
                reps=reps,
                workout=self.workout,
            )
            self.session.add(exercise)

        self.session.commit()
        self.destroy()


def open_new_workout(root, session):
    exercise_names = [e.name for e in session.query(MD.ExerciseName).all()]
    WorkoutEditor(parent=root, session=session, exercise_names=exercise_names)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    engine = create_engine(
        "sqlite+pysqlite:///workout_lab.db",
        echo=False,
        future=True,
    )
    MD.Base.metadata.create_all(engine)
    with MD.Session(engine) as session:
        open_new_workout(root, session)
        tk.mainloop()
