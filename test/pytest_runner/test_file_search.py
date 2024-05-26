from src.transpiler.compiler import Compiler as TC
from src.interpreter.compiler import Compiler as IC
from src.interpreter.syntax.semantics import *
from test.pytest_runner.forTest import *
import pytest

def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/versionError/file_search.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成し、実行
    with pytest.raises(TypeError) as e:
        result_t = TC(code,False,False).get_result_fullpath()
        # result_i = IC(code,False).get_result_fullpath()
    assert str(e.value) == "Inconsistent Version Usage:\nComparing Hash!1 and Hash!2 values"
