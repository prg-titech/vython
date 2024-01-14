from src.parser import Parser
from src.larkToIR import LarkToCustomAST
from src.interpreter import Interpreter
from src.syntax.semantics import resolve_heap_object

class Compiler:
    def __init__(self, code, debug_mode=False):
        self.debug_mode = debug_mode
        self.code = code
        self.ast = None
        self.ir = None
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
        interpreter = Interpreter(debug_mode = self.debug_mode)
        result_index = interpreter.interpret(self.ir)
        self.heap = interpreter.heap
        self.result = resolve_heap_object(self.heap, result_index)

    def get_result(self):
        return self.result

    def get_result_fullpath(self):
        self.parse()
        self.compile_to_ir()
        self.evaluate()
        result = self.get_result()
        return result