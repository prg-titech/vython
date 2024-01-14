from src.syntax.semantics import *
from src.syntax.language import *


class Interpreter:
    def __init__(self, debug_mode=False):
        self.heap = Heap()
        self.global_env = Environment()
        self.eval_depth = 0  # 評価の深さ（ネストレベル）
        self.step_count = 0  # 評価のステップ数
        self.debug_mode = debug_mode # デバッグモードがTrueのときのみ評価列を表示

        # Noneオブジェクトのための初期化処理
        # - Noneオブジェクトをヒープにアロケートし、そのインデックスを保存
        none_obj = VObject("None")
        self.none_index = self.heap.allocate(none_obj)

    def log_state(self, message, node, eval_depth, step_count, env=None, heap=None, result=None):
        step_info = f"[Step {step_count}]"
        node_info = f"----[Node]: {node}" if node else "None"
        env_info = f"-----[Env]: {env}" if env is not None else "No Env"
        heap_info = f"----[Heap]: {heap}" if heap is not None else "Empty Heap"
        result_info = f"--[Result]: {result}" if result is not None else ""

        indent = "|" * (eval_depth - 1)

        # 結果情報がある場合はresult, それ以外の場合はターゲットノードを出力
        print(f"{indent} {step_info} {message}")
        if result_info:
            print(f"{indent} {result_info}")
        else:
            print(f"{indent} {node_info}")
        print(f"{indent} {env_info}")
        print(f"{indent} {heap_info}")

    # ASTノードを評価するメソッド
    # ASTのオブジェクト名を利用して、適切なinterpret_*メソッドを呼び出す
    def interpret(self, node, env=None):
        if env is None:
            env = self.global_env

        # method_name と同名のメソッド実行
        method_name = "interpret_" + type(node).__name__
        method = getattr(self, method_name, self.generic_interpret)

        cur_step = self.step_count # 前後のログでステップカウントは同一にする
        self.eval_depth += 1
        self.step_count += 1
        if self.debug_mode:
            self.log_state(f"[Starting] Rule: {method_name}", node, self.eval_depth, cur_step, env, self.heap)

        result = method(node, env)

        if self.debug_mode:
            self.log_state(f"[Completed] Rule: {method_name}", node, self.eval_depth, cur_step, env, self.heap, result)
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
        last_result_index = None
        for n in node.body:
            last_result_index = self.interpret(n, env)
        # Moduleの評価結果は、Module bodyの最後の式・文の評価結果と同一と見做す
        return last_result_index

    # クラス定義の評価
    def interpret_ClassDef(self, node, env):
        # クラス名とバージョンを取得
        type_tag = node.name.id
        version_classdef = node.name.version

        # 基底クラスを評価（簡易版, 未実装）
        class_bases = [self.interpret(base) for base in node.bases]

        # クラスの本体（メソッドなど）を評価
        class_body = {}
        for element in node.body:
            if isinstance(element, FunctionDef):
                # メソッド名を取得
                method_name = element.name.id

                # メソッドオブジェクトをヒープにアロケート
                heap_index = self.allocate_FunctionDef(element, env)

                # メソッドのヒープインデックスを保存
                class_body[method_name] = heap_index

        # クラスオブジェクトを作成し、グローバル環境に登録
        class_obj = VObject("class", name=type_tag, bases=class_bases, body=class_body)
        heap_index = self.heap.allocate(class_obj)
        env.set(type_tag, version_classdef, heap_index)

        # None値が格納されたメモリ上へのポインタを返す
        return self.none_index

    # 関数定義の評価
    def interpret_FunctionDef(self, node, env):
        # FunctionDefノードをヒープにallocate
        heap_index = self.allocate_FunctionDef(node, env)

        # 関数オブジェクトのヒープインデックスを環境に登録
        env.set(node.name.id, None, heap_index)

        # None値が格納されたメモリ上へのポインタを返す
        return self.none_index

    # 関数定義とメソッド定義に共通のallocate処理
    def allocate_FunctionDef(self, node, env):
        function_name = node.name.id
        # 関数の引数名を取得
        arg_names = [arg.id for arg in node.args] if node.args else []

        # 関数オブジェクトの作成
        func_obj = VObject("function", name=function_name, args=arg_names, body=node.body)

        # 関数オブジェクトをヒープに格納し、そのインデックスを環境に設定
        heap_index = self.heap.allocate(func_obj)
        
        # 確保したヒープ領域のheap_indexを返す
        return heap_index

    # 代入文の評価
    def interpret_Assign(self, node, env):
        # RHSの式の評価
        evaluated_value_index = self.interpret(node.value, env)

        for target in node.targets:
            if isinstance(target, Name):
                # LHSが単純な変数名の場合、ヒープインデックスをそのまま使用
                env.set(target.id, None, evaluated_value_index)
            elif isinstance(target, Attribute):
                # LHSが属性参照の場合
                obj_heap_index = self.interpret(target.value, env)
                obj = self.heap.get(obj_heap_index)
                if not isinstance(obj, VObject):
                    raise TypeError("Only objects have attributes")

                # 属性に設定する値は、評価された値のヒープインデックスを参照
                obj.set_attribute(target.attr.id, evaluated_value_index)
            else:
                raise TypeError("Invalid assignment target")

        # None値が格納されたメモリ上へのポインタを返す
        return self.none_index

    # 式の評価
    def interpret_Expr(self, node, env):
        evaluated_value_index = self.interpret(node.value)
        return evaluated_value_index

    # 関数呼び出しの評価(インスタンス生成・メソッド呼び出し)
    def interpret_Call(self, node, env):
        callable_obj_index = self.interpret(node.func, env)
        callable_obj = self.heap.get(callable_obj_index)

        # callable_objがNoneの場合、エラーを発生させる
        if callable_obj is None:
            raise TypeError(f"Callable object is None. Unable to call: \n{node.func}")

        # インスタンス生成
        # - ClassDefで環境に入ったクラス定義を表すオブジェクトが参照された場合に起きる
        if callable_obj.type_tag == "class":
            # インスタンスオブジェクトのtype_tagにはインスタンス元のクラス名を入れる
            type_tag = callable_obj.attributes["name"]

            # インスタンスに含まれるメソッドをクラス定義からコピー
            instance_attributes = {
                method_name: method_obj
                for method_name, method_obj in callable_obj.attributes["body"].items()
            }

            # インスタンスオブジェクト作成
            instance = VObject(type_tag, **instance_attributes)

            # インスタンスをヒープに配置し、そのインデックスを取得
            heap_index = self.heap.allocate(instance)

            # __init__メソッドが存在する場合は、それを実行
            init_method_index = instance.get_attribute("__init__")
            if init_method_index is not None:
                init_method = self.heap.get(init_method_index)
                # メソッド実行のための環境を作成
                method_env = Environment(parent=env)

                # selfを現在のインスタンスにバインド
                method_env.set("self", None, heap_index)

                # 引数を評価し、ローカル環境にセット
                for arg_name, arg_value in zip(
                    init_method.attributes["args"], node.args
                ):
                    if arg_name is not None:
                        evaluated_arg = self.interpret(arg_value, method_env)
                        method_env.set(arg_name.id, None, evaluated_arg) # ネストクラスを定義するならこの実装ではマズいかも
                for statement in init_method.attributes["body"]:
                    self.interpret(statement, method_env)

            # オブジェクトが格納されているヒープへのindexを返す
            return heap_index

        # 関数の評価, オブジェクトから属性参照で取り出されたメソッド呼び出しのケースを含む
        elif callable_obj.type_tag == "function":
            # 新しいローカル環境を作成
            local_env = Environment(parent=env)

            # 変数 'self' にインスタンスのインデックスをバインド
            local_env.set("self", None, callable_obj_index)

            # 引数リストから 'self' を除外して、残りの引数を処理
            func_args_wo_self = [
                arg for arg in callable_obj.attributes["args"] if arg != "self"
            ]
            for arg_name, arg_value in zip(func_args_wo_self, node.args):
                if arg_value is not None:
                    evaluated_arg = self.interpret(arg_value, env)
                    local_env.set(arg_name, None, evaluated_arg)

            # 関数本体の実行
            # 最後の式・文の評価結果(の値へのヒープインデックス)が最終的な返り値
            result_index = self.none_index
            for statement in callable_obj.attributes["body"]:
                result_index = self.interpret(statement, local_env)
            return result_index

        else:
            # type_tag が "class" でも "function" でもないなら不正な関数呼び出し
            raise TypeError(f"Attribute {callable_obj.type_tag} is not a callable method")

    # 属性参照の評価
    def interpret_Attribute(self, node, env):
        obj_heap_index = self.interpret(node.value, env)

        # ヒープからオブジェクトを取得
        obj = self.heap.get(obj_heap_index)

        # 属性名が正しく取得されているか確認
        attr_name = node.attr.id if isinstance(node.attr, Name) else node.attr
        attr = obj.get_attribute(attr_name)

        if attr is None:
            raise AttributeError(
                f"VObject of type {obj.__class__.__name__} has no attribute '{attr_name}'"
            )

        # 属性が参照するオブジェクトのインデックスを返す
        return attr

    # 名前(変数)の評価
    def interpret_Name(self, node, env):
        # 環境走査のためのキーを取得
        var_name = node.id
        var_version = None
        if node.version is not None:
            var_version = node.version.version

        # 環境からヒープ上のインデックスを取得
        heap_index = env.get(var_name, var_version)
        # ヒープインデックスを返す
        return heap_index

    # リターン文の評価
    def interpret_Return(self, node, env):
        # リターン文は引数の式の評価結果をそのまま返す
        return self.interpret(node.value, env)

    # パス文の評価
    def interpret_Pass(self, node, env):
        # Pass文は何も計算しない
        # None値が格納されたメモリ上へのポインタを返す
        return self.none_index

    # Noneの評価
    def interpret_NoneNode(self, node, env):
        # None式は単にNoneノードを返す
        # None値が格納されたメモリ上へのポインタを返す
        return self.none_index

    # CallIncompatibleの評価
    def interpret_CallIncompatible(self, node, env):
        # 値のバージョンテーブルを操作するように変更する
        # 今はリターン文と同じ
        return self.interpret(node.value, env)

