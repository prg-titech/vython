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
    def __init__(self, vythonCode, transpile_mode, lazy_wrap=False, debug_mode=False):
        # コンパイルオプション
        self.transpile_mode = transpile_mode
        # - python
        # - vt-init
        # - vt-prop
        # - wrap-primitive
        # - vython

        # デバッグ用
        self.debug_mode = debug_mode

        # wrapを遅延する最適化を行う火のフラグ
        self.lazy_wrap = lazy_wrap

        # 評価の結果や途中で生成されるオブジェクト
        self.vythonCode = vythonCode
        self.vythonAST = None
        self.collected_classes = dict()
        self.pythonAST = None
        self.pythonCode = None
        self.result = None
        self.name_dict = {}
    
    # self.vythonCodeをparseしてvythonASTを作成
    def parse(self):
        if self.debug_mode:
            print(f"File Content:\n{self.vythonCode}")
        self.vythonAST = Parser(debug_mode = False).parse(self.vythonCode)
        if self.debug_mode:
            print(self.vythonAST)

    # self.vythonASTからバージョン空間を作成
    # 引数に応じて、2つのバージョンのみのバージョン空間に制限したものを返す
    def collect_classes(self, limit_version=True):
        collector = CollectClasses(self.debug_mode)
        collector.transform(self.vythonAST)
        if limit_version:
            self.collected_classes = collector.limit_version()
        else:
            self.collected_classes = collector.collected_classes

        if self.debug_mode:
            print(f"Collected Classes: {self.collected_classes}")
    
    # self.vythonASTをPython ASTにトランスパイルする
    # VIntなどのリテラルをラップするクラスの定義やDVC関数の定義が挿入される
    def transpile(self):
        if self.lazy_wrap:
            # tryとexceptの中に入るPython ASTをそれぞれ作成する
            transpiler_wo_wrap = Transpiler(self.collected_classes, "python", debug_mode=self.debug_mode)
            pythonAST_try = transpiler_wo_wrap.transform(self.vythonAST)
            transpiler = Transpiler(self.collected_classes, self.transpile_mode, debug_mode=self.debug_mode)
            pythonAST_except = transpiler.transform(self.vythonAST)
            # 作成したPythonASTを合成する
            handlers = [ast.ExceptHandler(type=None, name=None, body=pythonAST_except.body)]
            body = [ast.Try(body=pythonAST_try.body, handlers=handlers, orelse=None, finalbody=None)]
            pythonAST = ast.Module(body=body,type_ignores=[])
            self.pythonAST = pythonAST
        else:  
            transpiler = Transpiler(self.collected_classes, self.transpile_mode, debug_mode=self.debug_mode)
            self.pythonAST = transpiler.transform(self.vythonAST)

    # self.pythonASTをPythonのプログラムにunparseする
    def unparse(self):
        self.pythonCode = ast.unparse(self.pythonAST)
        if self.debug_mode:
            with open('output.py', 'w') as log:
                print("# [Unparse Python AST]",file=log)
                print(self.pythonCode, file=log)

    # self.pythonCodeを指定した名前空間のもとで実行する
    # 名前空間を指定しなかった場合は空で実行される
    # 返り値：self.result
    #   self.result["output"] : printで出力された内容
    #   self.result["error"]  : VersionErrorやPython runtimeによって出されたエラー
    # 　slef.result["dict"]   : 実行後の名前空間
    def execute(self, dict=None):
        output = io.StringIO()
        vython_output = None
        python_error = None
        try:
            with contextlib.redirect_stdout(output):
                if(dict is None):
                    self.clear_dict()
                    dict = self.name_dict
                exec(self.pythonCode, dict)
        except Exception as e:
            python_error = e
        vython_output = output.getvalue()
        self.result = (vython_output, python_error)
        self.result = {"output": vython_output, "error": python_error, "dict": dict}
        return self.result
    
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
    def evaluate_fullpath_time(self, python_code=None, name_dict=None):
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
