import tkinter as tk
from src.life_board import LifeBoard


class LifeApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Игра жизнь Конвея - вариант А-06")
        self.resizable(False, False)
        self.board = LifeBoard()
        tk.Label(self, text="Игра «Жизнь» Конвея", font=("Arial", 16, "bold")).pack(padx=24, pady=(24, 8))
        tk.Label(self, text="На этом этапе создана базовая структура приложения.").pack(padx=24, pady=(0, 24))


if __name__ == "__main__":
    LifeApp().mainloop()
