from src.transpiler.compiler import Compiler as TC
from helper_func import *
import pytest

@pytest.mark.DVC
def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/DVC/file_search.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成し、実行
    t = TC(code,"vython").run_fullpath()
    result = t.get_result()
    dict = t.get_dict()

    assert result.message == "Version Error 1:\nComputation between incompatible values created from Hash!1 and Hash!2: the hasher method has been updated in version 2 to change the algorithm used from SHA to MD5\n"
    assert isSameClass(result, "VersionError")
