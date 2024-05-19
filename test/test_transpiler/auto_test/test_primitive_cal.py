from src.transpiler.compiler import Compiler

def test():
    # テスト用のソースコードを読み込む
    with open("test/test_transpiler/sample/basic/primitive_cal.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成し、実行
    result = Compiler(code,False,False).get_result_fullpath()
    assert result == "19\n11\n60\n3.75\nHello World\nFalse\nTrue\nFalse\n"
