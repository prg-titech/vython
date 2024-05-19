from src.transpiler.compiler import Compiler

def test():
    # テスト用のソースコードを読み込む
    with open("test/test_transpiler/sample/basic/car_class.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成し、実行
    result = Compiler(code,False,False).get_result_fullpath()
    assert result == "Toyota\nCorolla\n2020\n30\n0\n"
