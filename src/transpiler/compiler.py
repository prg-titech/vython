import ast
import io
import contextlib
import time, traceback
from src.transpiler.vython_parser import Parser
from src.transpiler.transpiler.collect_classes import CollectClasses
from src.transpiler.transpiler.transpiler_to_vython import TranspilerToVython
from src.transpiler.transpiler.transpiler_to_python import TranspilerToPython
from src.transpiler.transpiler.transpiler_to_vtinit import TranspilerToVTInit
from src.transpiler.transpiler.transpiler_to_wrapprimitive import TranspilerToWrapPrimitive
from src.transpiler.transpiler.transpiler_to_vt_prop import TranspilerToVTProp
from src.transpiler.transpiler.test_transpiler import TestTranspiler

class Compiler:
    def __init__(self, vythonCode, transpile_mode, show_ast=False, debug_mode=False, ):
        # デバッグ用
        self.debug_mode = debug_mode
        self.show_ast = show_ast

        # コンパイルオプション
        self.transpile_mode = transpile_mode
        # - python
        # - vt-init
        # - vt-prop
        # - wrap-primitive
        # - vython
        # - test

        # 評価時に使用するオブジェクト
        self.vythonCode = vythonCode
        self.vythonAST = None
        self.collected_classes = dict()
        self.pythonAST = None
        self.pythonCode = None
        self.result = None
        self.created_obj = {}
    
    def parse(self):
        if self.debug_mode:
            print(f"File Content:\n{self.vythonCode}")
        self.vythonAST = Parser(debug_mode = False).parse(self.vythonCode)
        if self.debug_mode:
            print(self.vythonAST)

    def collect_classes(self, limit_version=True):
        collector = CollectClasses(self.debug_mode)
        collector.transform(self.vythonAST)
        if limit_version:
            self.collected_classes = collector.limit_version()
        else:
            self.collected_classes = collector.collected_classes

        if self.debug_mode:
            print(f"Collected Classes: {self.collected_classes}")
    
    def transpile(self):
        # transpile_modeに応じたTranspilerのディスパッチ
        match self.transpile_mode:
            case "python": transpiler = TranspilerToPython(self.collected_classes,self.debug_mode)
            case "wrap-primitive": transpiler = TranspilerToWrapPrimitive(self.collected_classes,self.debug_mode)
            case "vt-init": transpiler = TranspilerToVTInit(self.collected_classes,self.debug_mode)
            case "vt-prop": transpiler = TranspilerToVTProp(self.collected_classes,self.debug_mode)
            case "vython": transpiler = TranspilerToVython(self.collected_classes,self.debug_mode)
            # 新しい実装を試すとき用
            case "test": transpiler = TestTranspiler(self.collected_classes,self.debug_mode)
            # どれにも当てはまらない場合はvythonで実行
            case _: transpiler = TranspilerToVython(self.collected_classes,self.debug_mode)

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
        try:
            with contextlib.redirect_stdout(output):
                exec(self.pythonCode, self.created_obj)
        except Exception as e:
            self.result = e
            return self.result
        self.result = output.getvalue()
    
    def get_result(self):
        return self.result
    
    def get_dict(self):
        return self.created_obj

    def run_fullpath(self):
        self.parse()
        self.collect_classes(True)
        self.transpile()
        self.unparse()
        self.execute()
        return self
    
    # [評価用]: 評価用の特別な評価メソッド - evaluate_timeメソッドからしか使われない
    def execute_for_evaluate(self, mode):
        start_time = time.perf_counter()
        exec(self.pythonCode,self.created_obj)
        end_time = time.perf_counter()
        if mode == "generate":
            start_time = time.perf_counter()
            exec("main(m, f, y)",self.created_obj)
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
        self.collect_classes(True)
        end_time = time.perf_counter()
        execution_time["collect-classes"] = end_time - start_time

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
    
