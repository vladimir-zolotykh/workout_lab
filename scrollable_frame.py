#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, *, lock_x=False, lock_y=False, **kwargs):
        """
        lock_x: if True, inner frame width tracks canvas width (disables horizontal overflow)
        lock_y: if True, inner frame height tracks canvas height (disables vertical overflow)
        """
        super().__init__(parent, **kwargs)

        # Layout of this container: canvas (0,0), vbar (0,1), hbar (1,0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, highlightthickness=0, borderwidth=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.vbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.vbar.grid(row=0, column=1, sticky="ns")

        self.hbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.hbar.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(
            yscrollcommand=self.vbar.set, xscrollcommand=self.hbar.set
        )

        # The real content frame
        self.inner = ttk.Frame(self.canvas)
        self._win_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        # Track content size -> update scrollregion
        self.inner.bind("<Configure>", self._on_inner_configure)

        # Optionally lock width/height to suppress one axis of scrolling
        self.lock_x = lock_x
        self.lock_y = lock_y
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Mouse wheel support (enter/leave to bind/unbind)
        self.inner.bind("<Enter>", self._bind_mousewheel)
        self.inner.bind("<Leave>", self._unbind_mousewheel)

    # ----- sizing / scrollregion -----
    def _on_inner_configure(self, event):
        # Update scrollregion to encompass inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # Only lock the axis you ask for; otherwise allow overflow.
        if self.lock_x:
            self.canvas.itemconfig(self._win_id, width=event.width)
        if self.lock_y:
            self.canvas.itemconfig(self._win_id, height=event.height)

    # ----- mouse wheel bindings (Windows/macOS/Linux) -----
    def _bind_mousewheel(self, _event=None):
        # Vertical
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Win/macOS
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)  # Linux up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)  # Linux down
        # Horizontal with Shift+wheel
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_wheel)
        self.canvas.bind_all("<Shift-Button-4>", self._on_shift_wheel_linux)
        self.canvas.bind_all("<Shift-Button-5>", self._on_shift_wheel_linux)

    def _unbind_mousewheel(self, _event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")
        self.canvas.unbind_all("<Shift-MouseWheel>")
        self.canvas.unbind_all("<Shift-Button-4>")
        self.canvas.unbind_all("<Shift-Button-5>")

    def _on_mousewheel(self, event):
        # Windows: delta ±120 steps; macOS: smaller deltas (normalize by 120)
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def _on_shift_wheel(self, event):
        self.canvas.xview_scroll(int(-event.delta / 120), "units")

    def _on_mousewheel_linux(self, event):
        # event.num = 4 (up) / 5 (down)
        self.canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

    def _on_shift_wheel_linux(self, event):
        self.canvas.xview_scroll(-1 if event.num == 4 else 1, "units")


# -------------------- DEMO (grid-only) --------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("ScrollableFrame (grid)")
    # Constrain the window so content must overflow -> scrollbars prove they work
    root.geometry("800x450")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # lock_x=False to ALLOW horizontal scroll; lock_y=False to ALLOW vertical scroll
    sf = ScrollableFrame(root, lock_x=False, lock_y=False)
    sf.grid(row=0, column=0, sticky="nsew")

    # Populate with plenty of content to force both scrollbars
    for r in range(40):  # tall
        for c in range(30):  # wide
            ttk.Label(sf.inner, text=f"R{r}C{c}", relief="solid", padding=(6, 3)).grid(
                row=r, column=c, padx=2, pady=2, sticky="nsew"
            )

    # Optional: make columns expand inside the inner frame (purely visual)
    for c in range(30):
        sf.inner.columnconfigure(c, weight=1)

    root.mainloop()
