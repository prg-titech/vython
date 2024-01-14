from src.compiler import Compiler
from src.syntax.semantics import *

def test():
    # テスト用のソースコードを読み込む
    with open("test/sample/basic/ducktyping.py", "r") as f:
        source_code = f.read()

    # コンパイラのインスタンスを作成
    result = Compiler(source_code).get_result_fullpath()

    # 結果を検証
    assert isinstance(result, VObject)
    assert result.type_tag == "Swim"
    assert result.attributes == {}
