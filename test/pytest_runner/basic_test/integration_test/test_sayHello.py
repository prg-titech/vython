from src.transpiler.compiler import Compiler as TC
from helper_func import *
import pytest

@pytest.mark.integration
def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/integration/sayHello.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    t = TC(code,"vython").run_fullpath()
    result = t.get_result()
    dict = t.get_dict()

    # 結果を検証
    p1 = dict["person1"]
    p2 = dict["person2"]
    assert isSameValue(p1.name, "Alice")
    assert isSameValue(p1.age, 30)
    assert isSameValue(p1.greet(), "Hello, my name is Alice")
    assert isSameValue(p2.name, "Bob")
    assert isSameValue(p2.age, 25)
    assert isSameValue(p2.greet(), "Hello, my name is Bob")
