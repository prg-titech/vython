import sys

from src.parser import Parser
from src.larkToIR import LarkToCustomAST
from src.interpreter import Interpreter

# コマンドライン引数からファイル名を取得
if len(sys.argv) != 2:
    print("Incorrect arguments. Please specify a file name.")
    sys.exit(1)

path = sys.argv[1]

# ファイルの読み込み
try:
    with open(path, "r") as file:
        code = file.read()
except FileNotFoundError:
    print(f"The specified file '{path}' was not found.")
except Exception as e:
    print(f"An error occurred while opening the file: {e}")

print("=== File content:")
print(code)

# [Phase 1]: Parse to lark-python AST
print("=== Parse to lark-python AST")
ast = Parser().parse(code)
print(ast.pretty())

# [Phase 2]: Preprocess
# (今はint値とその上の二項演算をIntオブジェクトに変換しているだけ)
# ast_ = ArithmeticToMethod().transform(ast)
# print(ast_.pretty())

# [Phase 3]: Compile from lark-python AST to vython-IR AST
print("=== Compile to IR")
ir = LarkToCustomAST().transform(ast)
print(ir)

# [Phase 4]: Evaluate vython-IR AST on Interpreter
print("=== Evaluate")
result = Interpreter().interpret(ir)

print("\n[DEBUG] Evaluation succeeded!\n[DEBUG] Final result:")
print(result)
