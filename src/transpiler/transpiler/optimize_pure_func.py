import ast

class Pure_Func_Optimizer(ast.NodeTransformer):
    def __init__(self):
        pass

    def visit_Call(self, node):
        func = node.func
        args = node.args
        # 呼び出しているメソッドの名前がwrap literalクラスの名前である時、Constantに変換
        if (type(func) == ast.Name) and (func.id in ["VInt", "VFloat", "VStr", "VBool", "VList"]):
            return args[0]
        else:
            return node
