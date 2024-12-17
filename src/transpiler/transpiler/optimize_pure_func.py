import ast

class Pure_Func_Optimizer(ast.NodeTransformer):
    def __init__(self):
        pass

    def visit_Call(self, node):
        func = node.func
        args = node.args
        keywords = node.keywords
        # 呼び出しているメソッドの名前がwrap literalクラスの名前である時、Constantに変換
        if (type(func) == ast.Name) and (func.id in ["VInt", "VFloat", "VStr", "VBool"]):
            return args[0]
        elif (type(func) == ast.Name) and (func.id in ["VList"]):
            return self.visit(args[0])
        else:
            # generic_visitだと壊れるプログラムがある。
            # 特にargs以下のargがCallノードの時にvisit_Callが呼ばれない。
            transformed_func = self.visit(func)
            transformed_args = [self.visit(arg) for arg in args]
            transformed_keywords = [self.visit(keyword) for keyword in keywords]
            return ast.Call(func=transformed_func,args=transformed_args,keywords=transformed_keywords,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
