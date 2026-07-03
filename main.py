import tkinter as tk
from src.life_board import LifeBoard

CELL = 18


class LifeApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Игра жизнь Конвея - вариант А-06")
        self.board = LifeBoard(rows=25, cols=35)
        self.canvas = tk.Canvas(self, width=self.board.cols * CELL, height=self.board.rows * CELL, bg="white")
        self.canvas.grid(row=0, column=0, padx=12, pady=12)
        controls = tk.Frame(self)
        controls.grid(row=0, column=1, sticky="ns", padx=(0, 12), pady=12)
        self.info = tk.Label(controls, justify="left")
        self.info.pack(anchor="w", pady=(0, 12))
        tk.Button(controls, text="Следующее поколение", command=self.next_generation).pack(fill="x", pady=3)
        tk.Button(controls, text="Очистить", command=self.clear).pack(fill="x", pady=3)
        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.draw()

    def toggle_cell(self, event: tk.Event) -> None:
        row, col = event.y // CELL, event.x // CELL
        if self.board.in_bounds(row, col):
            self.board.toggle(row, col)
            self.draw()

    def next_generation(self) -> None:
        self.board.step()
        self.draw()

    def clear(self) -> None:
        self.board.clear()
        self.draw()

    def draw(self) -> None:
        self.canvas.delete("all")
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                x1, y1 = col * CELL, row * CELL
                color = "#293241" if self.board.is_alive(row, col) else "#f7f7f7"
                self.canvas.create_rectangle(x1, y1, x1 + CELL, y1 + CELL, fill=color, outline="#d5d5d5")
        self.info.config(text=f"Поколение: {self.board.generation}\nЖивых клеток: {len(self.board.alive)}")


if __name__ == "__main__":
    LifeApp().mainloop()
