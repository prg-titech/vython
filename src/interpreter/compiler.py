from src.interpreter.parser import Parser
from src.interpreter.larkToIR import LarkToCustomAST
from src.interpreter.interpreter import Interpreter
from src.interpreter.syntax.semantics import resolve_heap_object
import io
import contextlib
import time

class Compiler:
    def __init__(self, code, debug_mode=False):
        self.debug_mode = debug_mode
        self.code = code
        self.ast = None
        self.ir = None
        self.output = None
        self.result = None
        self.heap = None

    def set_debug_mode(self, debug_mode):
        self.debug_mode = debug_mode

    def parse(self):
        if self.debug_mode:
            print(f"File content:\n{self.code}")
        self.ast = Parser(debug_mode = self.debug_mode).parse(self.code)
        if self.debug_mode:
            print(self.ast.pretty())

    def compile_to_ir(self):
        self.ir = LarkToCustomAST(debug_mode = self.debug_mode).transform(self.ast)
        if self.debug_mode:
            print(self.ir)

    def evaluate(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output): 
            interpreter = Interpreter(debug_mode = self.debug_mode)
            result_index = interpreter.interpret(self.ir)
            self.heap = interpreter.heap
            self.result = resolve_heap_object(self.heap, result_index)
        captured_output = output.getvalue()
        self.output = captured_output

    def get_result(self):
        return self.result
    
    def get_output(self):
        return self.output

    # 結果を取得
    def get_result_fullpath(self):
        self.parse()
        self.compile_to_ir()
        self.evaluate()
        result = self.get_result()
        return result
    
    # printされた内容を取得
    def get_output_fullpath(self):
        self.parse()
        self.compile_to_ir()
        self.evaluate()
        output = self.output
        return output
    
    # [評価用]: fullpathの各段階での実行時間だけを返す
    def evaluate_time(self):
        execution_time = dict()

        start_time = time.time()
        self.parse()
        end_time = time.time()
        execution_time["parse"] = end_time - start_time

        start_time = time.time()
        self.compile_to_ir()
        end_time = time.time()
        execution_time["compile_to_ir"] = end_time - start_time

        start_time = time.time()
        self.evaluate()
        end_time = time.time()
        execution_time["execute"] = end_time - start_time

        return execution_time
    