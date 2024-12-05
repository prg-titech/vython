import ast
import io
import contextlib
import time, traceback
import lark
import copy
from src.transpiler.vython_parser import Parser
from src.transpiler.transpiler.collect_classes import CollectClasses
from src.transpiler.transpiler.transpiler import Transpiler

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

        # 評価時に使用するオブジェクト
        self.vythonCode = vythonCode
        self.vythonAST = None
        self.collected_classes = dict()
        self.pythonAST = None
        self.pythonCode = None
        self.result = None
        self.name_dict = {}
    
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
        transpiler = Transpiler(self.collected_classes, self.transpile_mode, self.debug_mode)
        self.pythonAST = transpiler.transform(self.vythonAST)
        if self.show_ast:
            print(ast.dump(self.pythonAST,False,indent=4))

    def transpile_wo_precode(self):
        transpiler = Transpiler(self.collected_classes, self.transpile_mode, self.debug_mode, True)
        self.pythonAST = transpiler.transform(self.vythonAST)
        if self.show_ast:
            print(ast.dump(self.pythonAST,False,indent=4))

    def unparse(self):
        self.pythonCode = ast.unparse(self.pythonAST)
        if self.debug_mode:
            with open('output.py', 'w') as log:
                print("# [Unparse Python AST]",file=log)
                print(self.pythonCode, file=log)

    def execute(self, dict=None):
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                if(dict is not None):
                    exec(self.pythonCode, dict)
                else:
                    self.clear_dict()
                    exec(self.pythonCode, self.name_dict)
        except Exception as e:
            self.result = e
            return self.result
        self.result = output.getvalue()

    def make_dict_of_precode(self):
        transpiler = Transpiler(self.collected_classes, self.transpile_mode, self.debug_mode)
        empty_vython_AST = lark.Tree(lark.Token('RULE', 'file_input'), [])
        python_AST = transpiler.transform(empty_vython_AST)
        python_code = ast.unparse(python_AST)
        dict_of_precode = {}
        exec(python_code, dict_of_precode)
        return dict_of_precode
    
    def get_result(self):
        return self.result
    
    def clear_dict(self):
        self.name_dict = {}

    def get_dict(self):
        return self.name_dict

    def run_fullpath(self):
        self.parse()
        self.collect_classes(True)
        self.transpile()
        self.unparse()
        self.execute()
        return self
    
    # [評価用]: 実行時間を測定
    def evaluate_execution_time_include_parse(self, python_code=None, name_dict=None):
        if(name_dict is None):
            name_dict = {}
        else:
            # deepcopyが望ましいが恐らくcopyで十分
            name_dict = copy.copy(name_dict)
        if(python_code is None):
            python_code = self.pythonCode
        start_time = time.perf_counter()
        exec(python_code, name_dict)
        end_time = time.perf_counter()
        return end_time - start_time

    def evaluate_execution_time(self, python_code=None, name_dict=None):
        if(name_dict is None):
            name_dict = {}
        else:
            # deepcopyが望ましいが恐らくcopyで十分
            name_dict = copy.copy(name_dict)
        if(python_code is None):
            python_code = self.pythonCode
        exec(python_code, name_dict)
        result = name_dict["exe_time"]
        return float(result)
    
    # [評価用]: DVC functionやwrap classの定義などを評価時間を含む時間を測定
    def evaluate_time(self, python_code=None, name_dict=None):
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

        execution_time["execute"] = self.evaluate_execution_time(python_code, name_dict)

        return execution_time
