from src.transpiler.compiler import Compiler as TC

def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/syntax/slice.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    result_t = TC(code,"vython").get_result_fullpath()

    # 結果を検証
    assert result_t == "[4, 5, 6, 7, 8, 9, 10, 11, 12]\n[1, 2, 3, 4, 5, 6, 7, 8]\n[5, 6, 7]\n[3, 5, 7, 9, 11]\n"
    