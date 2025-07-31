#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from sqlalchemy.orm import Session
from datetime import datetime
import model as MD
from showtext import file_io_redirected


def mark_command(func):
    func._is_command = True
    return func


class Dispatcher:
    commands: list[str] | None = None
    exercise_names: list[str] = [
        "front squat",
        "squat",
        "bench press",
        "deadlift",
        "pullup",
        "overhead press",
        "biceps curl",
    ]

    def __init__(self, session: Session, parent=None) -> None:
        self.session = session
        self.parent = parent
        self.ensure_commands_collected()

    @mark_command
    def init_exercises(self) -> None:
        for name in self.exercise_names:
            MD.ensure_exercise(self.session, name)
            self.session.commit()

    @mark_command
    @file_io_redirected
    def show_exercise_names(self):
        for ex_name in self.session.query(MD.ExerciseName).all():
            print(ex_name)

    @mark_command
    @file_io_redirected
    def show_workouts(self) -> None:
        for w in self.session.query(MD.Workout).all():
            print(w)

    @mark_command
    def add_squat_workout(self):
        workout = MD.Workout(started=datetime.now())
        new_exercise = MD.Exercise(
            weight=100.0,
            reps=5,
            workout=workout,
            exercise_name=MD.ensure_exercise(self.session, "squat"),
        )
        self.session.add(new_exercise)
        self.session.commit()

    @mark_command
    def remove_workout_id(self):
        workout = self.session.query(MD.Workout).get(10)
        self.session.delete(workout)
        self.session.commit()

    @classmethod
    def collect_commands(cls):
        cls.commands = [
            name
            for name, obj in cls.__dict__.items()
            if callable(obj) and getattr(obj, "_is_command", False)
        ]

    @classmethod
    def ensure_commands_collected(cls) -> list[str] | None:
        if not cls.commands:
            cls.collect_commands()
        return cls.commands
