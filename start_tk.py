#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from sqlalchemy import (
    Engine,
    create_engine,
)
import argparse
import argcomplete
import model as MD
import dispatcher as D


class Workout(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.dispatcher = kwargs.pop("dispatcher")
        super().__init__(*args, **kwargs)
        self.title("Workout lab")
        self.geometry("404x603+360+164")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        box = tk.Frame(self)
        box.grid(column=0, row=0)
        for name in D.Dispatcher.ensure_commands_collected():
            tk.Button(box, text=name, command=getattr(self.dispatcher, name)).grid(
                sticky="w"
            )

    def add_workout(self):
        pass


parser = argparse.ArgumentParser(
    description="Edit workout",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "--permanent-db", default="workout_lab.db", help="what db file to use"
)
parser.add_argument("--memory-db", help="use memory db")
parser.add_argument(
    "--echo", help="Show db commands", action="store_true", default=False
)

if __name__ == "__main__":
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    engine: Engine
    if args.memory_db:
        engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            echo=args.echo,
            future=True,
        )
    elif args.permanent_db:
        engine = create_engine(
            f"sqlite+pysqlite:///{args.permanent_db}",
            echo=args.echo,
            future=True,
        )
    else:
        raise RuntimeError("--permanent-db or --memory-db expected")

    MD.Base.metadata.create_all(engine)
    with MD.Session(engine) as session:
        dispatcher: D.Dispatcher = D.Dispatcher(session)
        Workout(dispatcher=dispatcher).mainloop()
