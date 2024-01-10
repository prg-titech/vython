from lark import Transformer, Tree

class ArithmeticToMethod(Transformer):
    def number(self, args):
        # 数字リテラルをIntオブジェクトのインスタンスに変換
        return Tree('funccall', ['Int', args[0]])

    def arith_expr(self, args):
        # 加算（+）と減算（-）
        return self._transform_operation(args, {'+': 'plus', '-': 'minus'})

    def term(self, args):
        # 乗算（*）、除算（/）、剰余演算（%）
        return self._transform_operation(args, {'*': 'multiply', '/': 'divide', '%': 'mod'})

    def factor(self, args):
        # 単項プラスとマイナス
        if args[0] in ['+', '-']:
            return Tree('funccall', [args[1], 'unary' + args[0]])
        return args[0]

    def power(self, args):
        # べき乗（**）
        if len(args) == 2:
            return Tree('funccall', [args[0], 'power', args[1]])
        return args[0]

    def _transform_operation(self, args, operations):
        if len(args) > 1:
            result = args[0]
            for i in range(1, len(args), 2):
                op = args[i]
                right = args[i + 1]
                method = operations.get(op)
                if method:
                    result = Tree('funccall', [
                        Tree('getattr', [result, Tree('name', [method])]), 
                        Tree('arguments', [right])
                    ])
            return result
        else:
            return args[0]