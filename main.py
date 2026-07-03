from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from src.life_board import LifeBoard
from src.storage import load_life_file, save_life_file

CELL = 18


class LifeApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Игра «Жизнь» Конвея — вариант А-06 Прохоров Денис Александрович БИС 24-3")
        self.board = LifeBoard(rows=25, cols=35)
        self.running = False
        self.after_id: str | None = None
        self.speed = tk.IntVar(value=250)

        root = ttk.Frame(self, padding=10)
        root.grid(sticky="nsew")
        self.canvas = tk.Canvas(root, width=self.board.cols * CELL, height=self.board.rows * CELL, bg="white", highlightthickness=1)
        self.canvas.grid(row=0, column=0, rowspan=2, padx=(0, 12))
        self.canvas.bind("<Button-1>", self.toggle_cell)

        controls = ttk.Frame(root)
        controls.grid(row=0, column=1, sticky="new")
        ttk.Label(controls, text="Управление", font=("Arial", 12, "bold")).grid(sticky="w", pady=(0, 8))
        ttk.Button(controls, text="Следующее поколение", command=self.next_generation).grid(sticky="ew", pady=2)
        self.start_button = ttk.Button(controls, text="Запустить", command=self.toggle_run)
        self.start_button.grid(sticky="ew", pady=2)
        ttk.Button(controls, text="Очистить", command=self.clear).grid(sticky="ew", pady=2)
        ttk.Button(controls, text="Загрузить глайдер", command=self.load_glider).grid(sticky="ew", pady=2)

        ttk.Separator(controls).grid(sticky="ew", pady=10)
        ttk.Label(controls, text="Скорость (мс)").grid(sticky="w")
        ttk.Scale(controls, from_=50, to=800, variable=self.speed, orient="horizontal").grid(sticky="ew")
        self.speed_label = ttk.Label(controls, text="250 мс")
        self.speed_label.grid(sticky="w")
        self.speed.trace_add("write", lambda *_: self.speed_label.config(text=f"{self.speed.get()} мс"))

        ttk.Separator(controls).grid(sticky="ew", pady=10)
        ttk.Button(controls, text="Сохранить состояние", command=self.save_state).grid(sticky="ew", pady=2)
        ttk.Button(controls, text="Загрузить состояние", command=self.load_state).grid(sticky="ew", pady=2)

        self.info = ttk.Label(root, justify="left")
        self.info.grid(row=1, column=1, sticky="sw", pady=(10, 0))
        self.draw()

    def toggle_cell(self, event: tk.Event) -> None:
        if self.running:
            return
        row, col = event.y // CELL, event.x // CELL
        if self.board.in_bounds(row, col):
            self.board.toggle(row, col)
            self.draw()

    def next_generation(self) -> None:
        self.board.step()
        self.draw()

    def tick(self) -> None:
        if not self.running:
            return
        self.next_generation()
        self.after_id = self.after(self.speed.get(), self.tick)

    def toggle_run(self) -> None:
        self.running = not self.running
        self.start_button.config(text="Остановить" if self.running else "Запустить")
        if self.running:
            self.tick()
        elif self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

    def clear(self) -> None:
        if self.running:
            self.toggle_run()
        self.board.clear()
        self.draw()

    def load_glider(self) -> None:
        self.clear()
        center_row, center_col = self.board.rows // 2, self.board.cols // 2
        for dr, dc in [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]:
            self.board.set_alive(center_row + dr, center_col + dc)
        self.draw()

    def save_state(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".life", filetypes=[("Life state", "*.life")])
        if path:
            save_life_file(self.board, path)

    def load_state(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Life state", "*.life")])
        if not path:
            return
        try:
            self.board = load_life_file(path)
            self.canvas.config(width=self.board.cols * CELL, height=self.board.rows * CELL)
            self.draw()
        except ValueError as error:
            messagebox.showerror("Ошибка загрузки", str(error))

    def draw(self) -> None:
        self.canvas.delete("all")
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                x1, y1 = col * CELL, row * CELL
                fill = "#27374D" if self.board.is_alive(row, col) else "#F5F7FA"
                self.canvas.create_rectangle(x1, y1, x1 + CELL, y1 + CELL, fill=fill, outline="#D6DCE4")
        self.info.config(text=(f"Поколение: {self.board.generation}\n"
                               f"Живых клеток: {len(self.board.alive)}\n"
                               "Правило: B3/S23"))


if __name__ == "__main__":
    LifeApp().mainloop()
