import sys
import time
from src.transpiler.compiler import Compiler

class CommandError(Exception):
    pass

def execute_phase(message, function):
    start_time = time.perf_counter()
    function()
    end_time = time.perf_counter()
    print(message)
    print(f"  --> Completed in {end_time-start_time:.4f} seconds")

def just_execute_phase(message, function):
    start_time = time.perf_counter()
    function()
    end_time = time.perf_counter()
    return end_time - start_time

def run(args):
    debug_mode = False
    show_ast = False
    transpile_mode = "vython"
    file_path = None

    # transpile_modeはコマンドラインの第二引数に来ることを想定
    # 指定されていないかったらデフォルトで"vython"のままとする
    match args[0]:
        case "vython": 
            transpile_mode = "vython"
            args = args[1:]
        case "python": 
            transpile_mode = "python"
            args = args[1:]
        case "vt-init": 
            transpile_mode = "vt-init"
            args = args[1:]
        case "wrap-primitive": 
            transpile_mode = "wrap-primitive"
            args = args[1:]
        case "vt-prop": 
            transpile_mode = "vt-prop"
            args = args[1:]
        case "test":
            transpile_mode = "test"
            args = args[1:]
        case _: pass

    try:
        for arg in args:
            if arg in ["--debug", "-d"]:
                debug_mode = True
            elif arg == "--ast":
                show_ast = True
            else:
                if file_path is not None:
                    print("Too many arguments. Please specify only one file name.")
                    sys.exit(1)
                file_path = arg
    except CommandError as e:
        print(f"Error: {e}")
        sys.exit(1)

        # 変換するコードを取得
    try:
        with open(file_path, "r") as file:
            code = file.read()
    except FileNotFoundError:
        print(f"The specified file '{file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while opening the file: {e}")
        sys.exit(1)

    compiler = Compiler(code, transpile_mode, show_ast, debug_mode)

    # 各フェーズの実行
    execute_phase("[Phase 1] Prase to lark-vython AST", lambda: compiler.parse())
    execute_phase("[Phase 1.5] Collect classes from lark-vython AST", lambda: compiler.collect_classes(True))
    execute_phase("[Phase 2] Transpile lark-vython AST to Python AST", lambda: compiler.transpile())
    execute_phase("[Phase 3] Unparse Python AST", lambda: compiler.unparse())
    execute_phase("[Phase 4] Execution", lambda: compiler.execute())
    print(f"[Result]:\n{compiler.get_result()}")
