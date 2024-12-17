import ast

class Pure_Func_Optimizer(ast.NodeTransformer):
    def __init__(self):
        pass

    def visit_Call(self, node):
        func = node.func
        args = node.args
        keywords = node.keywords
        # 呼び出しているメソッドの名前がwrap literalクラスの名前である時、Constantに変換
        if (type(func) == ast.Name) and (func.id in ["VInt", "VFloat", "VStr", "VBool", "VList"]):
            return args[0]
        else:
            func = self.generic_visit(func)
            args = [self.generic_visit(arg) for arg in args]
            keywords = [self.generic_visit(keyword) for keyword in keywords]
            return ast.Call(func=func,args=args,keywords=keywords,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
