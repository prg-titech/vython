from src.transpiler.compiler import Compiler as TC

def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/syntax/break_continue.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    result_t = TC(code,"vython").get_result_fullpath()

    # 結果を検証
    assert result_t == "0\n1\n2\n3\n4\n5\n6\n7\n8\n9\nhave not been breaked\n"
    
