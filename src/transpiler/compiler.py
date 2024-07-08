import ast
import io
import contextlib
import time
from src.transpiler.vython_parser import Parser
from src.transpiler.transpiler.transpiler_to_vython import TranspilerToVython
from src.transpiler.transpiler.transpiler_to_python import TranspilerToPython
from src.transpiler.transpiler.transpiler_to_vtinit import TranspilerToVTInit
from src.transpiler.transpiler.transpiler_to_wrapprimitive import TranspilerToWrapPrimitive
from src.transpiler.transpiler.transpiler_to_vt_synt import TranspilerToVTSynt

class Compiler:
    def __init__(self, vythonCode, transpile_mode, show_ast=False, debug_mode=False, ):
        # デバッグ用
        self.debug_mode = debug_mode
        self.show_ast = show_ast

        # コンパイルオプション
        self.transpile_mode = transpile_mode
        # - python
        # - vt-init
        # - vt-synt
        # - wrap-primitive
        # - vython

        # 評価時に使用するオブジェクト
        self.vythonCode = vythonCode
        self.vythonAST = None
        self.pythonAST = None
        self.pythonCode = None
        self.result = None
    
    def parse(self):
        if self.debug_mode:
            print(f"File Content:\n{self.vythonCode}")
        self.vythonAST = Parser(debug_mode = False).parse(self.vythonCode)
        if self.debug_mode:
            print(self.vythonAST)
    
    def transpile(self):
        # transpile_modeに応じたTranspilerのディスパッチ
        match self.transpile_mode:
            case "python": transpiler = TranspilerToPython(self.debug_mode)
            case "warp-primitive": transpiler = TranspilerToWrapPrimitive(self.debug_mode)
            case "vt-init": transpiler = TranspilerToVTInit(self.debug_mode)
            case "vt-synt": transpiler = TranspilerToVTSynt(self.debug_mode)
            case "vython": transpiler = TranspilerToVython(self.debug_mode)
            # どれにも当てはまらない場合はvythonで実行
            case _: transpiler = TranspilerToVython(self.debug_mode)

        self.pythonAST = transpiler.transform(self.vythonAST)
        if self.show_ast:
            print(ast.dump(self.pythonAST,False,indent=4))

    def unparse(self):
        self.pythonCode = ast.unparse(self.pythonAST)
        if self.debug_mode:
            with open('output.py', 'w') as log:
                print("# [Unparse Python AST]",file=log)
                print(self.pythonCode, file=log)

    def execute(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(self.pythonCode,globals())
        captured_output = output.getvalue()
        self.result = captured_output
        return self.result
    
    def get_result(self):
        return self.result

    def get_result_fullpath(self):
        self.parse()
        self.transpile()
        self.unparse()
        self.execute()
        return self.result
    
    # [評価用]: 評価用の特別な評価メソッド - evaluate_timeメソッドからしか使われない
    def execute_for_evaluate(self, mode):
        global_dict = globals()
        start_time = time.perf_counter()
        exec(self.pythonCode,global_dict)
        end_time = time.perf_counter()
        if mode == "generate":
            start_time = time.perf_counter()
            exec("main(m, f, y)",global_dict)
            end_time = time.perf_counter()
        return end_time - start_time
    
    # [評価用]: fullpathの各段階での実行時間だけを返す
    def evaluate_time(self, mode):
        execution_time = dict()

        start_time = time.perf_counter()
        self.parse()
        end_time = time.perf_counter()
        execution_time["parse"] = end_time - start_time

        start_time = time.perf_counter()
        self.transpile()
        end_time = time.perf_counter()
        execution_time["transpile"] = end_time - start_time

        start_time = time.perf_counter()
        self.unparse()
        end_time = time.perf_counter()
        execution_time["unparse"] = end_time - start_time

        execution_time["execute"] = self.execute_for_evaluate(mode)

        return execution_time
    
