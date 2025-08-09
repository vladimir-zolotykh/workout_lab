#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import model as MD

# from scrollableframe import ScrollableFrame
from scrolledframe import ScrolledFrame


@dataclass
class ExerciseLog:
    frame: ttk.Frame
    name_var: tk.StringVar
    weight_var: tk.DoubleVar
    reps_var: tk.IntVar


class WorkoutEditor(tk.Canvas):
    def __init__(
        self,
        parent,
        session: Session,
        exercise_names: list[str],
        workout: MD.Workout | None = None,
    ) -> None:
        self.parent = parent
        super().__init__(parent)
        self.session = session
        self.exercise_names = exercise_names  # list[str]
        self.workout = workout
        self.exercise_widgets: list[ExerciseLog] = []

        self.box = ttk.Frame(self)
        self.window_id = self.create_window((0, 0), window=self.box, anchor=tk.NW)
        self.box.columnconfigure(0, weight=1)

        ts_frame = ttk.Frame(self.box)
        ts_frame.grid(sticky=tk.W, padx=10, pady=5)
        ttk.Label(ts_frame, text="Started:").grid()
        self.timestamp_var = tk.StringVar()
        self.timestamp_var.set(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        ttk.Entry(ts_frame, textvariable=self.timestamp_var, state="readonly").grid()

        scrolled = ScrolledFrame(self.box)
        scrolled.grid(sticky=tk.NSEW, padx=10, pady=5)
        self.ex_frame = scrolled.scrolled_frame

        btn_frame = ttk.Frame(self.box)
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.grid(sticky=tk.EW, padx=10, pady=5)
        ttk.Button(btn_frame, text="Add Exercise", command=self.add_exercise).grid(
            sticky=tk.W
        )
        ttk.Button(
            btn_frame, text="Save Workout & Quit", command=self.save_workout
        ).grid(row=0, column=1)

        if self.workout:
            for ex in self.workout.exercises:
                self.add_exercise(exercise=ex)
        else:
            self.add_exercise()

    def add_exercise(self, exercise: MD.Exercise | None = None):
        frame = ttk.Frame(self.ex_frame)
        frame.grid(sticky=tk.EW, pady=2)

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
        cb.grid(row=0, column=0, padx=5)

        weight_entry = ttk.Entry(frame, textvariable=weight_var, width=7)
        weight_entry.grid(row=0, column=1, padx=5)
        reps_entry = ttk.Entry(frame, textvariable=reps_var, width=5)
        reps_entry.grid(row=0, column=2, padx=5)

        exlog: ExerciseLog = ExerciseLog(frame, name_var, weight_var, reps_var)
        del_btn = ttk.Button(
            frame, text="Delete", command=lambda: self.remove_exercise(exlog)
        )
        del_btn.grid(row=0, column=3, padx=5)

        self.exercise_widgets.append(exlog)

    def remove_exercise(self, exlog: ExerciseLog) -> None:
        self.exercise_widgets.remove(exlog)
        exlog.frame.destroy()

    def save_workout(self) -> None:
        # This method should create or update SQLAlchemy objects
        print("Saving workout:")
        started = datetime.strptime(self.timestamp_var.get(), "%Y-%m-%d %H:%M:%S")

        if not self.workout:
            self.workout = MD.Workout(started=started)
            self.session.add(self.workout)
        else:
            self.workout.exercises.clear()  # reset if editing

        for exlog in self.exercise_widgets:
            ex_name = exlog.name_var.get()
            weight = exlog.weight_var.get()
            reps = exlog.reps_var.get()
            ex_name_obj: MD.ExerciseName = MD.ensure_exercise(self.session, ex_name)
            exercise = MD.Exercise(
                exercise_name=ex_name_obj,
                weight=weight,
                reps=reps,
                workout=self.workout,
            )
            self.session.add(exercise)

        self.session.commit()
        self.quit()


def open_workout(root: tk.Tk, session: Session, workout: MD.Workout | None):
    exercise_names: list[str] = [e.name for e in session.query(MD.ExerciseName).all()]
    WorkoutEditor(root, session, exercise_names=exercise_names, workout=workout)


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
        workout: MD.Workout | None = session.query(MD.Workout).first()
        open_workout(root, session, workout=workout)
        tk.mainloop()
