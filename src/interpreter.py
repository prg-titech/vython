from src.syntax.semantic_object import *
from src.syntax.language import *


class Interpreter:
    def __init__(self):
        self.heap = Heap()
        self.global_env = Environment()
        self.eval_depth = 0  # 評価の深さ（ネストレベル）

    def log_state(self, message, node, eval_depth, env=None, result=None):
        indent = "|" * eval_depth
        node_info = f"Node: {node}" if node else "None"
        env_info = f"Env: {env}" if env is not None else "No Env"
        result_info = f"Result: {result}" if result is not None else ""

        # 結果情報がある場合のみ、その行を出力
        if result_info:
            print(
                f"{indent} {message}\n{indent} {node_info}\n{indent} {env_info}\n{indent} {result_info}"
            )
        else:
            print(f"{indent} {message}\n{indent} {node_info}\n{indent} {env_info}")

    # ASTノードを評価するメソッド
    # ASTのオブジェクト名を利用して、適切なinterpret_*メソッドを呼び出す
    def interpret(self, node, env=None):
        if env is None:
            env = self.global_env

        self.eval_depth += 1
        method_name = "interpret_" + type(node).__name__
        method = getattr(self, method_name, self.generic_interpret)

        self.log_state(f"[Starting]", node, self.eval_depth, env)

        result = method(node, env)

        self.log_state(f"[Completed]", node, self.eval_depth, env, result)
        self.eval_depth -= 1

        return result

    # 未定義ASTが引数に来た場合の挙動
    def generic_interpret(self, node, env):
        error_msg = f"No interpret_{type(node).__name__} method defined.\n"
        error_msg += f"Node details: {node}\n"
        if hasattr(node, "__dict__"):
            error_msg += f"Node attributes: {node.__dict__}"
        else:
            error_msg += "Node has no attribute dictionary."
        raise Exception(error_msg)

    #########################################
    ### 以下各種ASTノードの評価方法を定義 ###
    #########################################

    # Moduleの評価
    def interpret_Module(self, node, env):
        last_result = None
        for n in node.body:
            last_result = self.interpret(n, env)
        return last_result

    # クラス定義の評価
    def interpret_ClassDef(self, node, env):
        class_name = node.name.id  # クラス名を取得
        class_bases = [self.interpret(base) for base in node.bases]  # 基底クラスを評価（簡易版）

        # クラスの本体（メソッドなど）を評価
        class_body = {}
        for element in node.body:
            if isinstance(element, FunctionDef):
                method_name = element.name.id
                method_obj = Object(
                    "function", name=method_name, args=element.args, body=element.body
                )
                class_body[method_name] = method_obj

        # クラスオブジェクトを作成し、グローバル環境に登録
        class_obj = Object("class", name=class_name, bases=class_bases, body=class_body)
        env.set(class_name, class_obj)
        return Void()

    # 関数定義の評価
    def interpret_FunctionDef(self, node, env):
        # 関数の引数名を取得（node.argsが引数のリストを持つことを確認）
        arg_names = [arg.id for arg in node.args.args] if node.args else []
        # 関数オブジェクトの作成
        func_obj = Object("function", name=node.name.id, args=arg_names, body=node.body)
        # 関数を環境に設定
        env.set(node.name.id, func_obj)
        return Void()

    # 代入文の評価
    def interpret_Assign(self, node, env):
        value = self.interpret(node.value, env)
        for target in node.targets:
            if isinstance(target, Name):
                # 単純な変数名の場合
                env.set(target.id, value)
            elif isinstance(target, Attribute):
                # 属性参照の場合
                obj = self.interpret(target.value, env)
                if not isinstance(obj, Object):
                    raise TypeError("Only objects have attributes")
                obj.set_attribute(target.attr, value)
            else:
                raise TypeError("Invalid assignment target")
        return Void()

    # 式の評価
    def interpret_Expr(self, node, env):
        return self.interpret(node.value)

    # 関数呼び出しの評価(メソッド含む)
    def interpret_Call(self, node, env):
        callable_obj = self.interpret(node.func, env)
        # callable_objがNoneの場合、エラーを発生させる
        if callable_obj is None:
            raise TypeError(f"Callable object is None. Unable to call: \n{node.func}")

        # クラスのインスタンス化
        # 注：ClassDefで環境に入ると、class定義は特別なタグ"class"のついたオブジェクトとして格納される
        if callable_obj.type_tag == "class":
            # クラス名を取得
            class_name = callable_obj.attributes["name"]

            # クラスのメソッドをインスタンスにコピー
            instance_attributes = {}
            for method_name, method_obj in callable_obj.attributes["body"].items():
                instance_attributes[method_name] = method_obj

            # インスタンスを生成し、生成元のクラス名をtype_tagとして設定
            instance = Object(class_name, **instance_attributes)

            # __init__があるときは実行
            init_method = instance.get_attribute("__init__")
            if init_method:
                method_env = Environment(parent=env)
                method_env.set("self", instance)
                for arg_name, arg_value in zip(
                    init_method.attributes["args"], node.args
                ):
                    if arg_name is not None:
                        evaluated_arg = self.interpret(arg_value, method_env)
                        method_env.set(arg_name.id, evaluated_arg)

                for statement in init_method.attributes["body"]:
                    self.interpret(statement, method_env)
            return instance

        # インスタンスのメソッド呼び出し
        elif callable_obj.type_tag == "instance":
            method = callable_obj.get_attribute(node.func.attr)
            if method and method.type_tag == "function":
                # メソッドの実行環境を設定
                method_env = Environment(parent=env)
                method_env.set("self", callable_obj)

                # メソッド引数の処理
                for arg_def, arg_val in zip(method.attributes["args"], node.args):
                    evaluated_arg = self.interpret(arg_val, method_env)
                    method_env.set(arg_def.id, evaluated_arg)

                # メソッド本体の実行
                for statement in method.attributes["body"]:
                    result = self.interpret(statement, method_env)
                    if isinstance(result, Return):
                        return result.value
            else:
                raise TypeError(f"Attribute {node.func.attr} is not a callable method")

        # 関数の評価
        elif callable_obj.type_tag == "function":
            # 新しいローカル環境を作成
            local_env = Environment(parent=env)

            # 引数をローカル環境に設定
            # 'self' 引数を除外して、残りの引数を処理
            # 注：適当にzipしているが、二引数以上の関数で順序がどうなるのかわからん(バグるかも)
            func_args_wo_self = [
                arg for arg in callable_obj.attributes["args"] if arg.id != "self"
            ]
            for arg_name, arg_value in zip(func_args_wo_self, node.args):
                if arg_value is not None:
                    evaluated_arg = self.interpret(arg_value, env)
                    local_env.set(arg_name.id, evaluated_arg)

            # 関数本体の実行
            result = None
            for statement in callable_obj.attributes["body"]:
                result = self.interpret(statement, local_env)
            return result

        else:
            raise TypeError(f"Object {callable_obj} is not callable")

    # 属性参照の評価
    def interpret_Attribute(self, node, env):
        obj = self.interpret(node.value)
        # 属性名が正しく取得されているか確認
        attr_name = node.attr.id if isinstance(node.attr, Name) else node.attr
        attr = obj.get_attribute(attr_name)
        if attr is None:
            raise AttributeError(
                f"Object of type {type(obj).__name__} has no attribute '{attr_name}'"
            )
        return attr

    # 名前(変数)の評価
    def interpret_Name(self, node, env):
        return env.get(node.id)

    # リターン文の評価
    def interpret_Return(self, node, env):
        return self.interpret(node.value, env)

    # パス文の評価
    def interpret_Pass(self, node, env):
        return Void()

    # Noneの評価
    def interpret_NoneNode(self, node, env):
        return None
