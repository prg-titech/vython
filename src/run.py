import sys
from src.compiler import Compiler

def main():
    if len(sys.argv) != 2:
        print("Incorrect arguments. Please specify a file name.")
        sys.exit(1)

    path = sys.argv[1]

    try:
        with open(path, "r") as file:
            code = file.read()
    except FileNotFoundError:
        print(f"The specified file '{path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while opening the file: {e}")
        sys.exit(1)

    print("=== File content:")
    print(code)

    compiler = Compiler()
    print("=== Parse to lark-python AST")
    compiler.parse(code)

    print("=== Compile to IR")
    compiler.compile_to_ir()

    print("=== Evaluate")
    compiler.evaluate()

    print("\n[DEBUG] Evaluation succeeded!\n[DEBUG] Final result:")
    print(compiler.get_result())

if __name__ == "__main__":
  main()
