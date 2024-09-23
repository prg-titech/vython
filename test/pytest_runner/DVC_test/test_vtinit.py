from src.transpiler.compiler import Compiler as TC

def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/DVC/vtinit.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成し、実行
    result_t = TC(code, "vython").get_result_fullpath()

    assert result_t == "1\n4\nFalse\n"