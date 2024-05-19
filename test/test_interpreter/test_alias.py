from src.interpreter.compiler import Compiler
from src.interpreter.syntax.semantics import *

def test():
    # テスト用のソースコードを読み込む
    with open("test/test_interpreter/sample/basic/alias.py", "r") as f:
        source_code = f.read()

    # コンパイラのインスタンスを作成
    result = Compiler(source_code).get_result_fullpath()

    # 結果を検証
    assert isinstance(result, VObject)
    assert result.type_tag == "Apple"
    assert result.attributes == {}
