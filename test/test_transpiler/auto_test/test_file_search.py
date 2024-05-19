import pytest
from src.transpiler.compiler import Compiler

def test():
    # テスト用のソースコードを読み込む
    with open("test/test_transpiler/sample/incompat/file_search.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成し、実行
    with pytest.raises(TypeError) as e:
        result = Compiler(code,False,False).get_result_fullpath()
    assert str(e.value) == "Inconsistent Version Usage:\nComparing Hash!1 and Hash!2 values"
