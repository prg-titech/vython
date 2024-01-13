import sys
import time
from src.compiler import Compiler

def execute_phase(message, function):
    start_time = time.time()
    function()
    end_time = time.time()
    print(message)
    print(f"  --> Completed in {end_time - start_time:.2f} seconds")

def main():
    debug_mode = False
    file_path = None

    # コマンドライン引数の処理
    for arg in sys.argv[1:]:
        if arg in ["--debug", "-d"]:
            debug_mode = True
        else:
            if file_path is not None:
                print("Too many arguments. Please specify only one file name.")
                sys.exit(1)
            file_path = arg

    try:
        with open(file_path, "r") as file:
            code = file.read()
    except FileNotFoundError:
        print(f"The specified file '{file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while opening the file: {e}")
        sys.exit(1)

    compiler = Compiler(code, debug_mode = debug_mode)

    # 各フェーズの実行
    execute_phase("[Phase 1] Parse to lark-python AST", lambda: compiler.parse())
    print("[Phase 2] Preprocess\n  --> Skipped")
    # execute_phase("Phase 2: Preprocessing", lambda: compiler.preprocess(code))
    execute_phase("[Phase 3] Compile to IR", lambda: compiler.compile_to_ir())
    execute_phase("[Phase 4] Interpretation", lambda: compiler.evaluate())

    print(f"[Result]\n  {compiler.get_result()}")

if __name__ == "__main__":
  main()
