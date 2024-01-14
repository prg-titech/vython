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
        return ClassDef(name=name, version=version, bases=bases, body=body)

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

    def funccall(self, items):
        func, args = items[0], self._flatten_list(items[1:])
        transformed_func = self.transform(func) if isinstance(func, Tree) else func

        # transformed_funcがAttributeで、そのattrが"incompatible"の場合、特別なASTに変換
        if (isinstance(transformed_func, Attribute) and 
            isinstance(transformed_func.attr, Name) and 
            transformed_func.attr.id == "incompatible"):
            return CallIncompatible(value=transformed_func.value)
        else:
            return Call(func=transformed_func, version=None, args=args)

    def funccallwithversion(self, items):
        func, version, args = items[0], items[1], self._flatten_list(items[2:])
        transformed_func = self.transform(func) if isinstance(func, Tree) else func
        return Call(func=transformed_func, version=version, args=args)

    def version(self, items):
        number = items[0]
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
        return Name(id=id)

    def name(self, items):
        id = items[0].value
        return Name(id=id)

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
