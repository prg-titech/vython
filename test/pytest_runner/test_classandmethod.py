from src.transpiler.compiler import Compiler as TC
from src.interpreter.compiler import Compiler as IC
from src.interpreter.syntax.semantics import *
from test.pytest_runner.forTest import *

def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/classandmethod.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    result_i = IC(code,False).get_result_fullpath()
    result_t = TC(code,False,False).get_result_fullpath()

    # 結果を検証
    assert isinstance(result_i, VObject)
    assert result_i.type_tag == "D"
    # dunderメソッドを持ち運ばなくなったため
    # init_method = result.attributes["__init__"]
    # assert init_method.type_tag == "function"
    # assert init_method.attributes["args"] == ["self"]
    # assert isinstance(init_method.attributes["body"][0], Pass)