from lark import Token, Transformer, Tree
from src.syntax.language import *


class LarkToCustomAST(Transformer):
    def __init__(self, debug_mode=False):
        # 今の所使ってない
        self.debug_mode = debug_mode

    def file_input(self, items):
        return Module(body=self._flatten_list(items))

    def classdef(self, items):
        name, version, bases, body = items[0], items[1], [], self._flatten_list(items[3:])
        # バージョン付きクラスは名前にバージョン属性を付与する
        if isinstance(name, Name):
            name.version = version
        return ClassDef(name=name, bases=bases, body=body)

    def assign_stmt(self, items):
        assign_tree = items[0]
        targets = assign_tree.children[0]
        value = assign_tree.children[1]

        transformed_targets = (
            self.transform(targets) if isinstance(targets, Tree) else targets
        )
        transformed_value = self.transform(value) if isinstance(value, Tree) else value

        return Assign(targets=[transformed_targets], value=transformed_value)

    def expr_stmt(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        return Expr(value=transformed_value)
    
    def const_true(self, items):
        return ConstTrue()
    
    def const_false(self, items):
        return ConstFalse()
    
    def string(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        return String(transformed_value)

    def number(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        return Number(transformed_value)
    
    def comp_op(self, items):
        value = items[0]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        return CompOp(transformed_value)
    
    def comparison(self, items):
        transformed_values = []
        # 
        for item in items:
            transformed_value = self.transform(item) if isinstance(item, Tree) else item
            transformed_values.append(transformed_value)
        return Comparison(transformed_values)
    
    def or_expr(self, items):
        value_left = items[0]
        value_right = items[1]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        return OrExpr(transformed_value_l, transformed_value_r)
    
    def and_expr(self, items):
        value_left = items[0]
        value_right = items[1]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        return AndExpr(transformed_value_l, transformed_value_r)

    def arith_expr(self, items):
        value_left = items[0]
        op = items[1]
        value_right = items[2]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        transformed_op = self.transform(op) if isinstance(op, Tree) else op
        return ArithExpr(transformed_value_l, transformed_value_r, transformed_op)

    def term(self, items):
        value_left = items[0]
        op = items[1]
        value_right = items[2]
        transformed_value_l = self.transform(value_left) if isinstance(value_left, Tree) else value_left
        transformed_value_r = self.transform(value_right) if isinstance(value_right, Tree) else value_right
        transformed_op = self.transform(op) if isinstance(op, Tree) else op
        return Term(transformed_value_l, transformed_value_r, transformed_op)
    
    def factor(self, items):
        op = items[0]
        value = items[1]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        transformed_op = self.transform(op) if isinstance(op, Tree) else op
        return Factor(transformed_op, transformed_value)
    
    # if文astの変換
    def if_stmt(self, items):
        test = items[0]
        then_body = items[1]
        elifs = items[2]
        else_body = items[3]
        transformed_test = self.transform(test) if isinstance(test, Tree) else test
        transformed_then_body = self.transform(then_body) if isinstance(then_body, Tree) else then_body
        transformed_elifs = self.transform(elifs) if isinstance(elifs, Tree) else elifs
        transformed_else_body = self.transform(else_body) if isinstance(else_body, Tree) else else_body
        return If(transformed_test, transformed_then_body, transformed_elifs, transformed_else_body)
    
    def elifs(self, items):
        return Elifs(elif_=self._flatten_list(items))
    
    def elif_(self, items):
        test = items[0]
        then_body = items[1]
        transformed_test = self.transform(test) if isinstance(test, Tree) else test
        transformed_then_body = self.transform(then_body) if isinstance(then_body, Tree) else then_body
        return Elif(transformed_test, transformed_then_body)

    def funccall(self, items):
        func, args = items[0], self._flatten_list(items[1:])
        transformed_func = self.transform(func) if isinstance(func, Tree) else func

        # transformed_funcがAttributeで、そのattrが"incompatible"の場合、特別なASTに変換
        if (isinstance(transformed_func, Attribute) and 
            isinstance(transformed_func.attr, Name) and 
            transformed_func.attr.id == "incompatible"):
            return CallIncompatible(value=transformed_func.value, args=args)
        else:
            return Call(func=transformed_func, args=args)

    def funccallwithversion(self, items):
        func, version, args = items[0], items[1], self._flatten_list(items[2:])
        transformed_func = self.transform(func) if isinstance(func, Tree) else func
        # バージョン付きインスタンス生成の場合はNameオブジェクトにバージョンを入れる
        if isinstance(transformed_func, Name):
            transformed_func.version = version
        return Call(func=transformed_func, args=args)

    def version(self, items):
        number = items[0][0]
        return Version(version=number)

    def getattr(self, items):
        value, attr = items[0], items[1]
        transformed_value = self.transform(value) if isinstance(value, Tree) else value
        transformed_attr = self.transform(attr) if isinstance(attr, Tree) else attr
        return Attribute(value=transformed_value, attr=transformed_attr)

    def arguments(self, items):
        args = []
        for item in items:
            if isinstance(item, Tree):
                args.append(self.transform(item))
            else:
                args.append(item)
        return args

    def var(self, items):
        # 'var' ルールの中の 'name' ルールに対応する Tree オブジェクトから直接文字列を取得
        id = items[0].id
        return Name(id=id, version=None)

    def name(self, items):
        id = items[0].value
        return Name(id=id, version=None)

    def suite(self, items):
        return self._flatten_list(items)

    def parameters(self, items):
        return [item for item in items if item is not None]

    # def funcdef(self, items):
    #     name, params_tree, _, body = items
    #     # 'params_tree' が Tree オブジェクトかどうかを確認
    #     if isinstance(params_tree, Tree):
    #         args = [self.transform(param) for param in params_tree.children if isinstance(param, Tree)]
    #     else:
    #         # 'params_tree' がリストの場合、直接イテレート
    #         args = [self.transform(param) for param in params_tree if isinstance(param, Tree)]
    #     return FunctionDef(name=name, args=args, body=self._flatten_list(body))

    def funcdef(self, items):
        name, params_tree, _, body = items
        # 'params_tree' が Tree オブジェクトの場合
        if isinstance(params_tree, Tree):
            # params_treeの子ノードから引数を取得
            args = [self.transform(param) for param in params_tree.children]
        else:
            # params_treeがリストでない場合、空の引数リストを設定
            args = params_tree
        return FunctionDef(name=name, args=args, body=self._flatten_list(body))

    def return_stmt(self, items):
        value_item = items[0]
        value = (
            self.transform(value_item) if isinstance(value_item, Tree) else value_item
        )
        return Return(value=value)

    def pass_stmt(self, _):
        return Pass()

    def const_none(self, _):
        return NoneNode()

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
