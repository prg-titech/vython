from src.transpiler.compiler import Compiler as TC
from helper_func import *
import pytest

@pytest.mark.integration
def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/integration/ducktyping.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    t = TC(code,"vython").run_fullpath()
    result = t.get_result()
    dict = t.get_dict()

    # 結果を検証
    animal = dict["Animal_v_1"]()
    bird = dict["bird"]
    fish = dict["fish"]
    assert isSameClass(animal.make_it_move(bird), "Fly_v_1")
    assert isSameClass(animal.make_it_move(fish), "Swim_v_1")
