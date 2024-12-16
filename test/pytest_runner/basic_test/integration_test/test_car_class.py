from src.transpiler.compiler import Compiler as TC
from helper_func import *
import pytest

@pytest.mark.integration
def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/integration/car_class.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    t = TC(code,"vython").run_fullpath()
    result = t.get_result()['output']
    dict = t.get_dict()

    # 結果を検証
    car = dict["car"]
    assert isSameValue(car.make, "Toyota")
    assert isSameValue(car.model, "Corolla")
    assert isSameValue(car.year, 2020)
    # メソッド呼び出しはprintを通してしか検証できない
    # assert isSameValue(car.accelerate(30), 30)
    # assert isSameValue(car.brake(40), 0)
