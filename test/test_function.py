from src.syntax.language import Pass
from src.compiler import Compiler
from src.syntax.semantic_object import VObject

def test():
    # テスト用のソースコードを読み込む
    with open("test/sample/basic/function.py", "r") as f:
        source_code = f.read()

    # コンパイラのインスタンスを作成
    result = Compiler(source_code).get_result_fullpath()

    # 結果を検証
    assert isinstance(result, VObject)
    assert result.type_tag == "C"