from lark import Token, Transformer, Tree
import ast
import copy

global_func_paths = {"src/transpiler/lib/python_lib/global_func.py"}
primitive_classes = {"src/transpiler/lib/wrap_primitive_lib/primitive_lib/Primitive_Bool.py","src/transpiler/lib/wrap_primitive_lib/primitive_lib/Primitive_String.py","src/transpiler/lib/wrap_primitive_lib/primitive_lib/Primitive_Number.py"}

# larkToIRを参考に実装する
class TranspilerToWrapPrimitive(Transformer):
    def __init__(self, debug_mode):
        self.debug_mode = debug_mode
        
        # Python ASTに挿入するグローバル関数(VT操作/検査)をASTに変換
        global_func_asts = set()
        for global_func_path in global_func_paths:
            with open(global_func_path,"r") as file:
                global_func_code = file.read()
            global_func_asts.add(ast.parse(global_func_code))
        # トランスパイラインスタンスの属性として保持
        self.global_func_asts = global_func_asts

        # Primitiveクラスの定義をASTに変換
        primitive_class_asts = set()
        for primitive_class in primitive_classes:
            with open(primitive_class,"r") as file:
                primitive_class_code = file.read()
            primitive_class_asts.add(ast.parse(primitive_class_code))
        # トランスパイラインスタンスの属性として保持
        self.primitive_class_asts = primitive_class_asts

    def file_input(self, items):
        body = self._flatten_list(items)

        # Primitiveクラスを挿入
        for primitive_class_ast in self.primitive_class_asts:
            body.insert(0,primitive_class_ast)
        # グローバル関数を挿入
        for global_func_ast in self.global_func_asts:
            body.insert(0, global_func_ast)

        return ast.Module(body=body,type_ignores=[])

    def classdef(self, items):
        name, version, bases, body = items[0], items[1], [], self._flatten_list(items[3:])
        # バージョンの情報もクラス名が持つ
        class_name = str(name) + "_v_" + str(version)

        return ast.ClassDef(name=class_name,bases=[],keywords=[],body=body,decorator_list=[],type_params=[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def assign_stmt(self, items):
        assign_tree = items[0]
        targets = assign_tree.children[0]
        value = assign_tree.children[1]

        transformed_targets = (
            self.transform(targets) if isinstance(targets, Tree) else targets
        )
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        return ast.Assign(targets=[transformed_targets], value=transformed_value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def expr_stmt(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        return ast.Expr(value=transformed_value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    # primitiveを含むASTの変換(新)
    def const_true(self, items):
        value = ast.Constant(True,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        return ast.Call(ast.Name(id="Primitive_Bool_v_0",ctx=ast.Load()),[value],[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def const_false(self, items):
        value = ast.Constant(False,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        return ast.Call(ast.Name(id="Primitive_Bool_v_0",ctx=ast.Load()),[value],[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def string(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        transformed_value.value = transformed_value.value.replace('"',"")
        transformed_value = ast.Constant(transformed_value.value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        return ast.Call(ast.Name(id="Primitive_String_v_0",ctx=ast.Load()),[transformed_value],[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def number(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        if isinstance(transformed_value, Token):
            match transformed_value.type:
                case 'DEC_NUMBER': transformed_value = int(transformed_value.value)
                case 'FLOAT_NUMBER': transformed_value = float(transformed_value.value)
        transformed_value = ast.Constant(transformed_value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        return ast.Call(ast.Name(id="Primitive_Number_v_0",ctx=ast.Load()),[transformed_value],[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def comp_op(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        match transformed_value:
            case "==":
                transformed_op = ast.Eq()
            case "!=":
                transformed_op = ast.NotEq()
            case ">":
                transformed_op = ast.Gt()
            case "<":
                transformed_op = ast.Lt()
            case "<=":
                transformed_op = ast.LtE()
            case ">=":
                transformed_op = ast.GtE()
        return transformed_op

    def comparison(self, items):
        # 要素数が適切かどうかのチェック
        size = len(items)
        if(size%2==0 or size<3):
            raise TypeError("Vython->Python: Inappropriate form of comparison")
        
        value_left = items[0]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_ops = []
        transformed_comparators = []
        for i in range(1, size):
            if i%2==1:
                op = items[i]
                transformed_op = self.transform(op) if isinstance(op, Tree) else op
                transformed_ops.append(transformed_op)
            else:
                comparator = items[i]
                transformed_comparator = self.transform(comparator) if isinstance(comparator, Tree) else comparator
                transformed_comparators.append(transformed_comparator)
        return ast.Compare(left=transformed_value_l,ops=transformed_ops,comparators=transformed_comparators,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def or_test(self, items):
        value_left = items[0]
        value_right = items[1]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        
        return ast.BoolOp(ast.Or(), [transformed_value_l, transformed_value_r])
    
    def and_test(self, items):
        value_left = items[0]
        value_right = items[1]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        
        return ast.BoolOp(ast.And(), [transformed_value_l, transformed_value_r])

    def not_test(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        return ast.UnaryOp(ast.Not(), transformed_value)

    def arith_expr(self, items):
        # 要素数が適切かどうかのチェック
        size = len(items)
        if(size%2==0):
            raise TypeError("Vython->Python: Inappropriate form of arith_expr")

        if(size == 1):
            value = items[0]
            transformed_value = self.transform(value) if isinstance(value, Tree) else value
            return transformed_value
        else:
            value_right = items[size-1]
            op = items[size-2]
            transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
            transformed_op = self.transform(op) if isinstance(op, Tree) else op
            match transformed_op:
                case "+": transformed_op = ast.Add()
                case "-": transformed_op = ast.Sub()
            return ast.BinOp(self.arith_expr(items[:-2]),transformed_op,transformed_value_r,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        
    def term(self, items):
        # 要素数が適切かどうかのチェック
        size = len(items)
        if(size%2==0):
            raise TypeError("Vython->Python: Inappropriate form of arith_expr")

        if(size == 1):
            value = items[0]
            transformed_value = self.transform(value) if isinstance(value, Tree) else value
            return transformed_value
        else:
            value_right = items[size-1]
            op = items[size-2]
            transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
            transformed_op = self.transform(op) if isinstance(op, Tree) else op
            match transformed_op:
                case "*": transformed_op = ast.Mult()
                case "/": transformed_op = ast.Div()
                case "%": transformed_op = ast.Mod()
                case "//": transformed_op = ast.FloorDiv()
            return ast.BinOp(self.arith_expr(items[:-2]),transformed_op,transformed_value_r,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def factor(self, items):
        value_left = items[0]
        value_right = items[1]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        match transformed_value_l:
            case "+": op = ast.UAdd()
            case "-": op = ast.USub()
        return ast.UnaryOp(op,transformed_value_r,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def if_stmt(self, items):
        # testとbodyの実装
        test = items[0]
        then_body = items[1]
        transformed_test = self.transform(test) if isinstance(test, Tree) else test
        transformed_body = self.transform(then_body) if isinstance(then_body, Tree) else then_body

        elif_list = items[2]
        else_body = items[3]
        transformed_elif_list = self.transform(elif_list) if isinstance(elif_list, Tree) else elif_list
        transformed_else_body = self.transform(else_body) if isinstance(else_body, Tree) else else_body
        transformed_orelse = [make_if_ast(transformed_elif_list,transformed_else_body)]
        if transformed_orelse[0] is None:
            transformed_orelse = []

        return ast.If(test=transformed_test,body=transformed_body,orelse=transformed_orelse,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def elifs(self, items):
        return self._flatten_list(items)
    
    def elif_(self, items):
        test = items[0]
        then_body = items[1]
        transformed_test = self.transform(test) if isinstance(test, Tree) else test
        transformed_then_body = self.transform(then_body) if isinstance(then_body, Tree) else then_body
        return [transformed_test, transformed_then_body]

    def funccall(self, items):
        func, args = items[0], self._flatten_list(items[1:])
        transformed_func = self.transform(func) if isinstance(func, Tree) else func
        return ast.Call(func=transformed_func,args=args,keywords=[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def funccallwithversion(self, items):
        func, version, args = items[0], items[1], self._flatten_list(items[2:])

        # バージョンの情報もクラス名が持つ
        if isinstance(func,ast.Name):
            func.id = func.id + "_v_" + str(version)
        else:
            raise TypeError("syntax error")
        
        return ast.Call(func=func,args=args,keywords=[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def version(self, items):
        number = items[0]
        return str(number)

    def getattr(self, items):
        value, attr = items[0], items[1]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        transformed_attr = self.transform(attr) if isinstance(attr, Tree) else attr
        return ast.Attribute(value=transformed_value, attr=transformed_attr,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def arguments(self, items):
        args = []
        for item in items:
            if isinstance(item, Tree):
                args.append(self.transform(item))
            else:
                args.append(item)
        return args
    
    def var(self, items):
        id = items[0]
        return ast.Name(id=id,ctx=ast.Load(),lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def name(self, items):
        id = items[0].value
        return str(id)
    
    def suite(self, items):
        return self._flatten_list(items)

    def parameters(self, items):
        args = []
        for item in items:
            if item is not None:
                args.append(ast.arg(item,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0))
        return ast.arguments(posonlyargs=[],args=args,kwonlyargs=[],kw_defaults=[],defaults=[])

    def funcdef(self, items):
        name, params_tree, _, body = items
        # 'params_tree' が Tree オブジェクトの場合
        if isinstance(params_tree, Tree):
            # params_treeの子ノードから引数を取得
            args = [self.transform(param) for param in params_tree.children]
        else:
            # params_treeがリストでない場合、空の引数リストを設定
            args = params_tree
        return ast.FunctionDef(name=name, args=args, body=self._flatten_list(body),decorator_list=[],type_params=[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def return_stmt(self, items):
        value_item = items[0]
        value = (
            self.transform(value_item) if isinstance(value_item, Tree) else value_item
        )
        return ast.Return(value=value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def pass_stmt(self, _):
        return ast.Pass(lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    # 適切か怪しい
    def const_none(self, _):
        return ast.Constant(None,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    # _flatten_list メソッドの定義
    def _flatten_list(self, l):
        flattened = []
        for item in l:
            if isinstance(item, list):
                flattened.extend([subitem for subitem in item if subitem is not None])
            elif isinstance(item, Tree):
                flattened.append(item)
            elif item is not None:
                flattened.append(item)
        return flattened

def make_if_ast(elif_list, else_body):
        if len(elif_list) == 0:
            return else_body
        elif len(elif_list) == 2:
            test = elif_list[0]
            body = elif_list[1]
            orelse = else_body
        else:
            test = elif_list[0]
            body = elif_list[1]
            orelse = [make_if_ast(elif_list[2:],else_body)]
        return ast.If(test=test,body=body,orelse=orelse,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)