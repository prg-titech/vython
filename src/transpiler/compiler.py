import ast
import io
import contextlib
import time
from src.transpiler.vython_parser import Parser
from src.transpiler.transpiler import Transpiler

class Compiler:
    def __init__(self, vythonCode, transpile_mode, show_ast, debug_mode=False, ):
        self.debug_mode = debug_mode
        self.show_ast = show_ast
        self.transpile_mode = transpile_mode

        # 評価時に使用するオブジェクト
        self.vythonCode = vythonCode
        self.vythonaAST = None
        self.pythonAST = None
        self.pythonCode = None
        self.result = None
    
    def parse(self):
        if self.debug_mode:
            print(f"File Content:\n{self.vythonCode}")
        self.vythonaAST = Parser(debug_mode = False).parse(self.vythonCode)
        if self.debug_mode:
            print(self.vythonaAST)
    
    def transpile(self):
        self.pythonAST = Transpiler(self.debug_mode, self.transpile_mode).transform(self.vythonaAST)
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
        start_time = time.time()
        exec(self.pythonCode,global_dict)
        end_time = time.time()
        if mode == "gen-t":
            start_time = time.time()
            exec("main(m, f, y)",global_dict)
            end_time = time.time()
        return end_time - start_time
    
    # [評価用]: fullpathの各段階での実行時間だけを返す
    def evaluate_time(self, mode):
        execution_time = dict()

        start_time = time.time()
        self.parse()
        end_time = time.time()
        execution_time["parse"] = end_time - start_time

        start_time = time.time()
        self.transpile()
        end_time = time.time()
        execution_time["transpile"] = end_time - start_time

        start_time = time.time()
        self.unparse()
        end_time = time.time()
        execution_time["unparse"] = end_time - start_time

        execution_time["execute"] = self.execute_for_evaluate(mode)

        return execution_time
    
