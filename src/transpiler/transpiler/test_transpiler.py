from lark import Token, Transformer, Tree
import ast
import copy


primitive_classes = "src/transpiler/vython_API/primitives.py"
global_func_path = "src/transpiler/vython_API/DVC.py"

# AST templates
initialize_func_path = "src/transpiler/vython_API/ast_templates/initialize_func.py"

# --------------------------------------
# 不具合を起こすかもしれない箇所リスト
# - PythonASTオブジェクトのctxが適当!?
# --------------------------------------

# larkToIRを参考に実装する
class TestTranspiler(Transformer):
    ############################
    ############################
    # トランスパイラ初期化
    ############################
    ############################
    def __init__(self, incompatible_classes, debug_mode):
        # self.incompatible_classes = incompatible_classes
        self.incompatible_classes = {"A"}
        self.debug_mode = debug_mode
    
        # Python ASTに挿入するグローバル関数(VT操作/検査)をASTに変換
        with open(global_func_path,"r") as file:
            global_func_code = file.read()
        self.global_func_ast = ast.parse(global_func_code).body

        # Python ASTに挿入するVython Primitiveクラス定義のAST
        with open(primitive_classes,"r") as file:
            primitive_classes_code = file.read()
        self.primitive_classes_ast = ast.parse(primitive_classes_code)

        # 互換性を気にするクラス名の集合を宣言
        self.incompatible_classes_ast = ast.parse(f"{self.incompatible_classes}").body[0]


        # クラス定義のイニシャライザーのテンプレートAST
        with open(initialize_func_path,"r") as file:
            initialize_func_code = file.read()
        self.initialize_func_ast = ast.parse(initialize_func_code).body[0]


    ############################
    ############################
    # module
    ############################
    ############################

    def file_input(self, items):
        body = self._flatten_list(items)

        # Primitiveクラスを挿入
        body.insert(0, self.primitive_classes_ast)
        # グローバル関数を挿入
        body.insert(0, self.global_func_ast)
        # 互換性を気にするクラス名の集合を挿入
        body.insert(0, self.incompatible_classes_ast)

        return ast.Module(body=body,type_ignores=[])


    ############################
    ############################
    # stmt
    ############################
    ############################

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

    # + AsyncFunctionDef
    
    def classdef(self, items):
        name, version, bases, body = items[0], items[1], [], self._flatten_list(items[3:])
        # バージョンの情報もクラス名が持つ
        class_name = str(name) + "_v_" + str(version)

        # 互換性を気にするクラスでないなら直ちに終了
        if not name in self.incompatible_classes:
            return ast.ClassDef(name=class_name,bases=[],keywords=[],body=body,decorator_list=[],type_params=[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        
        # ユーザ定義のメソッドをラップするメソッドの配列
        wrapped_func_list = []
        is_init_exist = False

        # basesの中身を検査
        for element in body:
            if isinstance(element,ast.FunctionDef):
                # initializeメソッドAST に VT初期化関数呼び出しAST を挿入
                if(element.name == "__init__"):
                    element.decorator_list.append(ast.Name(id="_vt_init_decorator", ctx=ast.Load()))
                    is_init_exist = True
                # メソッドをラップし、VT書き換え関数呼び出しASTを挿入した新しいメソッドASTに変更する
                else:
                    element.decorator_list.append(ast.Name(id="_vt_concat_decorator1", ctx=ast.Load()))

        if not is_init_exist:
            initialize_func_ast = copy.deepcopy(self.initialize_func_ast)
            initialize_func_ast.decorator_list.append(ast.Name(id="_vt_init_decorator", ctx=ast.Load()))
            body.append(initialize_func_ast)

        return ast.ClassDef(name=class_name,bases=[],keywords=[],body=body,decorator_list=[],type_params=[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def return_stmt(self, items):
        value_item = items[0]
        value = (
            self.transform(value_item) if isinstance(value_item, Tree) else value_item
        )
        return ast.Return(value=value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    # + delete

    def assign_stmt(self, items):
        assign_tree = items[0]
        targets = assign_tree.children[0]
        value = assign_tree.children[1]

        transformed_targets = (
            self.transform(targets) if isinstance(targets, Tree) else targets
        )
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        return ast.Assign(targets=[transformed_targets], value=transformed_value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    # TypeAlias

    # AugAssign
    # AnnAssign

    # For
    # AsyncFor

    # While

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

    # With
    # AsyncWith

    # Match

    # Raise
    # Try
    # TryStar
    # Assert

    # Import
    # ImportFrom

    # Global
    # NonLocal

    def expr_stmt(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        return ast.Expr(value=transformed_value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def pass_stmt(self, _):
        return ast.Pass(lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    #  Break
    #  Continue


    ############################
    ############################
    # expr
    ############################
    ############################

    # -----------------------------
    # ----- Vython Primitives -----
    # -----------------------------
    def or_test(self, items):
        # value_left = items[0]
        # value_right = items[1]
        # transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        # transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        # # 糖衣として実装
        # or_test_ast = copy.deepcopy(self.calling_or_suger_ast)
        # or_test_ast.value.test.args[0] = transformed_value_l
        # or_test_ast.value.body.args[1] = transformed_value_l
        # or_test_ast.value.orelse.args[0].args[0].args[0] = transformed_value_r
        # or_test_ast.value.orelse.args[1] = transformed_value_l
        # or_test_ast.value.orelse.args[2] = transformed_value_r
        # return or_test_ast.value
        value_left = items[0]
        value_right = items[1]
        return ast.BoolOp(ast.Or(), [value_left, value_right])
    
    def and_test(self, items):
        # value_left = items[0]
        # value_right = items[1]
        # transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        # transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        # # 糖衣として実装
        # and_test_ast = copy.deepcopy(self.calling_and_suger_ast)
        # and_test_ast.value.test.operand.args[0] = transformed_value_l
        # and_test_ast.value.body.args[1] = transformed_value_l
        # and_test_ast.value.orelse.args[0].args[0].args[0] = transformed_value_r
        # and_test_ast.value.orelse.args[1] = transformed_value_l
        # and_test_ast.value.orelse.args[2] = transformed_value_r
        # return and_test_ast.value
        value_left = items[0]
        value_right = items[1]
        return ast.BoolOp(ast.And(), [value_left, value_right])

    def not_test(self, items):
        # value = items[0]
        # transformed_value = self.transform(value) if isinstance(value, Tree) else value
        # op = ast.Not()
        # return ast.Call(func=ast.Name(id='Primitive_Bool_v_0', ctx=ast.Load()), args=[ast.UnaryOp(op,transformed_value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)], keywords=[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        value = items[0]
        return ast.UnaryOp(ast.Not(), value)
  
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

    # Lambda
    # IfExp
    def dict(self, items):
        keys = []
        values = []
        for item in items:
            keys.append(item.children[0])
            values.append(item.children[1])
        return ast.Dict(keys=keys,values=values)

    def set(self, items):
        return ast.Set(items)
    # ListComp
    # SetComp
    # DictComp
    # GeneratorExp

    # Await
    # Yield
    # YieldFrom

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
    
    # FormattedValue
    # JoinedStr
    
    def const_true(self, items):
        value = ast.Constant(True,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        return ast.Call(ast.Name(id="VBool",ctx=ast.Load()),[value],[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def const_false(self, items):
        value = ast.Constant(False,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        return ast.Call(ast.Name(id="VBool",ctx=ast.Load()),[value],[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def string(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        transformed_value.value = transformed_value.value.replace('"',"")
        transformed_value = ast.Constant(transformed_value.value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
        return ast.Call(ast.Name(id="VStr",ctx=ast.Load()),[transformed_value],[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def number(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        if isinstance(transformed_value, Token):
            match transformed_value.type:
                case 'DEC_NUMBER': 
                    transformed_value = int(transformed_value.value)
                    transformed_value = ast.Constant(transformed_value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
                    return ast.Call(ast.Name(id="VInt",ctx=ast.Load()),[transformed_value],[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
                case 'FLOAT_NUMBER': 
                    transformed_value = float(transformed_value.value)
                    transformed_value = ast.Constant(transformed_value,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
                    return ast.Call(ast.Name(id="VFloat",ctx=ast.Load()),[transformed_value],[],lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)

    def getattr(self, items):
        value, attr = items[0], items[1]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        transformed_attr = self.transform(attr) if isinstance(attr, Tree) else attr
        return ast.Attribute(value=transformed_value, attr=transformed_attr,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    def getitem(self, items):
        structure = items[0]
        iterator = items[1]
        # # イテレーターがVython Primitiveになってしまう場合
        # if(isinstance(iterator,ast.Call)):
        #     iterator = iterator.args[0]
        return ast.Subscript(value=structure, slice=iterator,ctx=ast.Load())

    # Starred

    def name(self, items):
        id = items[0].value
        return str(id)
          
    def var(self, items):
        id = items[0]
        return ast.Name(id=id,ctx=ast.Load(),lineno=0,col_offset=0,end_lineno=0,end_col_offset=0)
    
    # List
    def list(self, items):
        return ast.List(elts=items,ctx=ast.Load())

    # Tuple
    def tuple(self, items):
        return ast.Tuple(elts=items,ctx=ast.Load())

    # Slice


    ############################
    ############################
    # expr_context
    ############################
    ############################

    # Load
    # Store
    # Del


    ############################
    ############################
    # Other(tmp)
    ############################
    ############################

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
    
    def version(self, items):
        number = items[0]
        return str(number)

    def arguments(self, items):
        args = []
        for item in items:
            if isinstance(item, Tree):
                args.append(self.transform(item))
            else:
                args.append(item)
        return args

    def suite(self, items):
        return self._flatten_list(items)

    def parameters(self, items):
        args = []
        for item in items:
            if item is not None:
                args.append(ast.arg(item,lineno=0,col_offset=0,end_lineno=0,end_col_offset=0))
        return ast.arguments(posonlyargs=[],args=args,kwonlyargs=[],kw_defaults=[],defaults=[])

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
    
    
# ASTを変換する際の補助関数
def insert_vt_init_into_init_method(calling_vt_init_ast, element):
    tmp_ast = copy.deepcopy(calling_vt_init_ast)
    tmp_ast[0].value.args[0].id = element.args.args[0].arg
    element.body.append(tmp_ast)
    return element

def generate_wrap_method_ast(calling_vt_append_ast, wrapped_method_ast):
    result_ast = copy.deepcopy(calling_vt_append_ast)
    wrap_func_name = wrapped_method_ast.name
    wrapped_func_name = "__wrapped_" + wrap_func_name + "__"
    formal_args = wrapped_method_ast.args.args
    # wrapメソッドのASTを作成
    result_ast.name = wrap_func_name
    result_ast.args = wrapped_method_ast.args
    actual_args = []
    for formal_arg in formal_args:
        actual_args.append(ast.Name(id=formal_arg.arg,ctx=ast.Load()))
    result_ast.body[0].value.func.value = ast.Name(id=formal_args[0].arg,ctx=ast.Load())
    result_ast.body[0].value.func.attr = wrapped_func_name
    result_ast.body[0].value.args = actual_args[1:]
    result_ast.body[1].body[0].value.args[1]=actual_args[0]

    return result_ast

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