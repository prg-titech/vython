from src.parser import Parser
from src.larkToIR import LarkToCustomAST
from src.interpreter import Interpreter
from src.syntax.semantic_object import resolve_heap_object

class Compiler:
    def __init__(self):
        self.ast = None
        self.ir = None
        self.result = None
        self.heap = None

    def parse(self, code):
        self.ast = Parser().parse(code)
        print(self.ast.pretty())

    def compile_to_ir(self):
        self.ir = LarkToCustomAST().transform(self.ast)
        print(self.ir)

    def evaluate(self):
        interpreter = Interpreter()
        result_index = interpreter.interpret(self.ir)
        self.heap = interpreter.heap
        self.result = resolve_heap_object(self.heap, result_index)

    def get_result(self):
        return self.result
