from src.life_board import LifeBoard
from src.storage import load_life_file, save_life_file


def test_save_and_load_round_trip(tmp_path):
    original = LifeBoard(4, 5, {(0, 1), (2, 3)})
    path = tmp_path / "state.life"
    save_life_file(original, path)
    restored = load_life_file(path)
    assert restored.rows == 4
    assert restored.cols == 5
    assert restored.alive == {(0, 1), (2, 3)}


def test_invalid_state_file_is_rejected(tmp_path):
    path = tmp_path / "bad.life"
    path.write_text("3 3\n..x\n...\n...\n", encoding="utf-8")
    try:
        load_life_file(path)
    except ValueError as exc:
        assert "недопустимые" in str(exc)
    else:
        raise AssertionError("Ожидалась ошибка формата")
