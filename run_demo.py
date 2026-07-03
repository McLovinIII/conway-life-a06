from src.life_board import LifeBoard

board = LifeBoard(5, 5, {(2, 1), (2, 2), (2, 3)})
print(f"Поколение {board.generation}, живых клеток: {len(board.alive)}")
board.step()
print(f"Поколение {board.generation}, живых клеток: {len(board.alive)}")
print("Живые клетки:", sorted(board.alive))
