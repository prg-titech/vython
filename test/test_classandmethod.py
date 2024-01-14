from src.syntax.language import Pass
from src.compiler import Compiler
from src.syntax.semantics import VObject

def test():
    # テスト用のソースコードを読み込む
    with open("test/sample/basic/classandmethod.py", "r") as f:
        source_code = f.read()

    # コンパイラのインスタンスを作成
    result = Compiler(source_code).get_result_fullpath()

    # 結果を検証
    assert isinstance(result, VObject)
    assert result.type_tag == "D"
    init_method = result.attributes["__init__"]
    assert init_method.type_tag == "function"
    assert init_method.attributes["args"] == ["self"]
    assert isinstance(init_method.attributes["body"][0], Pass)