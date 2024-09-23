from src.transpiler.compiler import Compiler as TC

def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/integration/loop2.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    result_t = TC(code,"vython").get_result_fullpath()

    # 結果を検証
    assert result_t == "3628800\n"
