from src.interpreter.syntax.semantics import *
from src.interpreter.syntax.language import *
from src.interpreter.compatibilitychecker import *
from src.interpreter.primitive_lib.Primitive_lib import *
from src.interpreter.lib.global_func import *
import re
import copy

special_classes = {"number","string","bool"}

class Interpreter:
    def __init__(self, debug_mode=False):
        self.heap = Heap()
        self.global_env = Environment()
        self.eval_depth = 0  # 評価の深さ（ネストレベル）
        self.step_count = 0  # 評価のステップ数
        self.debug_mode = debug_mode # デバッグモードがTrueのときのみ評価列を表示

        # Noneオブジェクトのための初期化処理
        # - Noneオブジェクトをヒープにアロケートし、そのインデックスを保存
        none_obj = VObject("None", VersionTable("None", 0, False))
        self.none_index = self.heap.allocate(none_obj)

        # primitive libraryの読み込み
        # Number lib
        num_class_body = {}
        for element in number_member_list:
            method_name = element[0]
            method_def = element[1]
            heap_index = self.heap.allocate(method_def)
            num_class_body[method_name] = heap_index
        class_obj = VObject("class", VersionTable("number", 0, False), name="number", bases=[], body=num_class_body)
        heap_index = self.heap.allocate(class_obj)
        self.global_env.set("number", Version(0), heap_index)

        # String lib
        str_class_body = {}
        for element in string_member_list:
            method_name = element[0]
            method_def = element[1]
            heap_index = self.heap.allocate(method_def)
            str_class_body[method_name] = heap_index
        class_obj = VObject("class", VersionTable("string", 0, False), name="string", bases=[], body=str_class_body)
        heap_index = self.heap.allocate(class_obj)
        self.global_env.set("string", Version(0), heap_index)

        # Boolean lib
        boolean_class_body = {}
        for element in boolean_member_list:
            method_name = element[0]
            method_def = element[1]
            heap_index = self.heap.allocate(method_def)
            boolean_class_body[method_name] = heap_index
        class_obj = VObject("class", VersionTable("bool", 0, False), name="bool", bases=[], body=boolean_class_body)
        heap_index = self.heap.allocate(class_obj)
        self.global_env.set("bool", Version(0), heap_index)

        # global_funcの読み込み
        for element in global_func_list:
            func_def = element
            func_name = element.attributes["name"]
            heap_index = self.heap.allocate(func_def)
            self.global_env.set(func_name,None,heap_index)

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

                # メソッドオブジェクトをヒープにアロケート(関数定義)
                heap_index = self.allocate_MethodDef(element, env, type_tag, int(version_classdef.version))

                # メソッドのヒープインデックスを保存
                class_body[method_name] = heap_index

        # クラスオブジェクトを作成し、グローバル環境に登録
        class_obj = VObject("class", VersionTable(type_tag, int(version_classdef.version), False), name=type_tag, bases=class_bases, body=class_body)
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

    # 関数定義のallocate処理
    def allocate_FunctionDef(self, node, env):
        function_name = node.name.id
        # 関数の引数名を取得
        arg_names = [arg.id for arg in node.args] if node.args else []

        # 関数オブジェクトの作成
        func_obj = VObject("function", VersionTable("NormalFunction", 0, False), name=function_name, args=arg_names, body=node.body, partial_args=[])

        # 関数オブジェクトをヒープに格納し、そのインデックスを環境に設定
        heap_index = self.heap.allocate(func_obj)
        
        # 確保したヒープ領域のheap_indexを返す
        return heap_index
    
    # メソッド定義用のallocate処理
    def allocate_MethodDef(self, node, env, c, v):
        function_name = node.name.id
        # 関数の引数名を取得
        arg_names = [arg.id for arg in node.args] if node.args else []

        # 関数オブジェクトの作成
        func_obj = VObject("function", VersionTable(c, v, False), name=function_name, args=arg_names, body=node.body, partial_args=[])

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
        evaluated_value_index = self.interpret(node.value, env)
        return evaluated_value_index
    
        obj_index = self.interpret(node.value)
        obj = self.heap.get(obj_index)

        # objがTruthyかFalthyかの分類：ここで明示的に分類
        if((obj.type_tag=="bool") | (obj.type_tag=="number") | (obj.type_tag=="string")):
            if(obj.attributes["value"]):
                boolean_obj_index = self.interpret(Call(func=Name("bool", Version(0)),args=[True]), env)
                boolean_obj = self.heap.get(boolean_obj_index)
                boolean_obj.version_table.append(obj.version_table)
                return boolean_obj_index
            else:
                boolean_obj_index = self.interpret(Call(func=Name("bool", Version(0)),args=[False]), env)
                boolean_obj = self.heap.get(boolean_obj_index)
                boolean_obj.version_table.append(obj.version_table)
                return boolean_obj_index
        elif(obj.type_tag=="None"):
            boolean_obj_index = self.interpret(Call(func=Name("bool", Version(0)),args=[False]), env)
            boolean_obj = self.heap.get(boolean_obj_index)
            boolean_obj.version_table.append(obj.version_table)
            return boolean_obj_index
        else:
            boolean_obj_index = self.interpret(Call(func=Name("bool", Version(0)),args=[True]), env)
            boolean_obj = self.heap.get(boolean_obj_index)
            boolean_obj.version_table.append(obj.version_table)
            return boolean_obj_index

    # if文の評価
    def interpret_If(self, node, env):
        obj_test_index = self.interpret(node.test, env)
        obj_test = self.heap.get(obj_test_index)

        # obj_testが真ならnode.thenを、偽ならnode.elifs,node,elseを、type-tag!=boolならTyepErrorを出す
        result = self.none_index
        if(obj_test.type_tag != "bool"):         # testの評価値がbool出ない時
            raise TypeError("boolean value is required in test of If_stmt")
        elif(obj_test.attributes["value"]):      # testの評価値がTrueの時
            for n in node.then_body:
                obj_then_body_index = self.interpret(n, env)
                result = obj_then_body_index
        else:                                    # testの評価値がFalseの時
            obj_elifs_index = self.interpret(node.elifs)
            if(obj_elifs_index < 0):
                for n in node.else_body:
                    obj_else_body_index = self.interpret(n, env)
                    result = obj_else_body_index

        return result
    
    def interpret_Elifs(self, node, env):
        result = -1
        for n in node.elif_:
            if(result < 0):
                obj_elif_index = self.interpret(n, env)
                result = obj_elif_index
            else:
                return result
            
        return result

    def interpret_Elif(self, node, env):
        obj_test_index = self.interpret(node.test, env)
        obj_test = self.heap.get(obj_test_index)

        # このelif節のthenが評価されていない場合、返るindexは-1になる
        result = -1
        if(obj_test.type_tag != "bool"):         # testの評価値がbool出ない時
            raise TypeError("boolean value is required in test of If_stmt")
        elif(obj_test.attributes["value"]):      # testの評価値がTrueの時
            for n in node.then_body:
                obj_then_body_index = self.interpret(n, env)
                result = obj_then_body_index
        else:                                    # testの評価値がFalseの時
            pass

        return result

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
            # 特殊メソッドは除く
            dunder_method_name = r'^__.*__$'
            instance_attributes = {
                method_name: method_obj
                for method_name, method_obj in callable_obj.attributes["body"].items()
                if not bool(re.fullmatch(dunder_method_name, method_name))
            }

            # インスタンスのクラスとバージョンを環境のクラス定義から得る
            instance_vt = callable_obj.version_table

            # インスタンスオブジェクト作成
            instance = VObject(type_tag, VersionTable(instance_vt.vt[0][0], instance_vt.vt[0][1], False), **instance_attributes)

            # インスタンスをヒープに配置し、そのインデックスを取得
            heap_index = self.heap.allocate(instance)

            # __init__メソッドが存在する場合は、それを実行
            init_method_index = None
            for method_name, method_obj in callable_obj.attributes["body"].items():
                if method_name == '__init__':
                    init_method_index = method_obj
            if init_method_index is not None:
                init_method = self.heap.get(init_method_index)
                # メソッド実行のための環境を作成
                method_env = Environment(parent=env)

                # メソッド定義の引数リストの深いコピーを作成し、selfを除去
                args_copy = copy.deepcopy(init_method.attributes["args"])
                first_arg = args_copy.pop(0)

                # selfを現在のインスタンスにバインド
                method_env.set(first_arg, None, heap_index)

                # 引数を評価し、ローカル環境にセット
                for arg_name, arg_value in zip(
                    args_copy, node.args
                ):
                    if (arg_name is not None):
                        evaluated_arg = self.interpret(arg_value, method_env)
                        method_env.set(arg_name, None, evaluated_arg) # ネストクラスを定義するならこの実装ではマズいかも
                for statement in init_method.attributes["body"]:
                    self.interpret(statement, method_env)

            # primitive classだけ特別な値をattributesに配置
            if instance.type_tag in special_classes:
                instance.attributes["value"] = node.args[0]

            # オブジェクトが格納されているヒープへのindexを返す
            return heap_index

        # 関数オブジェクトの評価
        # オブジェクトから属性参照で取り出されたメソッド呼び出しも含む
        elif callable_obj.type_tag == "function":
            # 新しいローカル環境を作成
            local_env = Environment(parent=env)

            # 引数処理
            func_args = [
                arg
                for arg in callable_obj.attributes["args"]
            ]
            # partial_argsが空でない場合 => この評価をメソッド呼び出しとする
            # 仮引数の第一引数を、pariail_argsに保存された実引数で束縛する
            if(len(callable_obj.attributes["partial_args"])):
                first_formal_arg_name = callable_obj.attributes["args"][0]
                local_env.set(first_formal_arg_name, None, callable_obj.attributes["partial_args"][0])
                # 引数リストから 先頭要素 を消去
                func_args = func_args[1:]
            # 残りの仮引数を実引数で束縛する
            for arg_name, arg_value in zip(func_args, node.args):
                if arg_value is not None:
                    evaluated_arg = self.interpret(arg_value, env)
                    local_env.set(arg_name, None, evaluated_arg)

            # 関数本体の実行
            # 最後の式・文の評価結果(の値へのヒープインデックス)が最終的な返り値
            if(len(callable_obj.attributes["partial_args"])):
                call_instance_obj = self.heap.get(callable_obj.attributes["partial_args"][0])
                # 関数が特別なクラスに定義されたメソッドである場合
                if(call_instance_obj.type_tag in special_classes):
                    left_obj_index = local_env.get("left", None)
                    right_obj_index = local_env.get("right", None)
                    left_obj = self.heap.get(left_obj_index)
                    right_obj = self.heap.get(right_obj_index)
                    result_obj = callable_obj.attributes["body"][0](left_obj.attributes["value"], right_obj.attributes["value"])

                    # 互換性検査 & VT書き換え
                    checkCompatibility(left_obj.version_table, right_obj.version_table)
                    result_obj.version_table.append(left_obj.version_table)
                    result_obj.version_table.append(right_obj.version_table)

                    result_index = self.heap.allocate(result_obj)
                # それ以外のメソッド
                else:
                    for statement in callable_obj.attributes["body"]:
                        result_index = self.interpret(statement, local_env)
                    result_obj = self.heap.get(result_index)
                    result_obj.version_table.append(call_instance_obj.version_table)
                    self.heap.insert(result_obj, result_index)
            # TOPレベル関数の実行
            else:
                for statement in callable_obj.attributes["body"]:
                    result_index = self.interpret(statement, local_env)
            return result_index

        # 標準組み込み関数オブジェクトの評価
        elif callable_obj.type_tag == "global_function":
            # 実引数を評価し、bodyに適用
            actual_args = []
            for arg_value in node.args:
                if arg_value is not None:
                    evaluated_arg_index = self.interpret(arg_value, env)
                    evaluated_arg = self.heap.get(evaluated_arg_index)
                    actual_args.append(evaluated_arg)

            result_obj = callable_obj.attributes["body"][0](*actual_args)
            if result_obj is not None:
                result_index = self.heap.allocate(result_obj)
                return result_index
            else:
                return self.none_index

        # エラー 
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

        # 属性名がdunderである時 -> 特殊メソッドをクラス定義に取りにいく
        dunder_pattern = r'^__.*__$'
        if bool(re.fullmatch(dunder_pattern, attr_name)):
            # バージョンを0にしているが良くない
            heap_index = env.get(obj.type_tag, 0)
            class_obj = self.heap.get(heap_index)
            for method_name, method_obj in class_obj.attributes["body"].items():
                if method_name == attr_name:
                    attr = method_obj
        else:
            attr = obj.get_attribute(attr_name)

        if attr is None:
            raise AttributeError(
                f"VObject of type {obj.__class__.__name__} has no attribute '{attr_name}'"
            )
        
        attr_obj = self.heap.get(attr)
        # 属性参照の結果が関数であった場合、selfにobj_indexをバインドした部分関数を返す
        if(attr_obj.type_tag=="function"):
            result_obj = VObject("function", 
                                 attr_obj.version_table, 
                                 name=attr_obj.attributes["name"], 
                                 args=attr_obj.attributes["args"], 
                                 body=attr_obj.attributes["body"], 
                                 partial_args=[obj_heap_index])
            result_obj_index = self.heap.allocate(result_obj)
            return result_obj_index
        # 属性が参照するオブジェクトのインデックスを返す
        else:
            return attr

    # BoolOpの評価
    def interpret_BoolOp(self, node, env):
        op = node.op
        nodes = node.values
        node_l = nodes[0]
        node_r = nodes[1]
        obj_true = VObject("bool", VersionTable("bool", 0, False), value=True)
        obj_false = VObject("bool", VersionTable("bool", 0, False), value=False)

        # leftのbool値の計算
        # NoneもTrueになってしまう
        try:
            func_l_index = self.interpret(node_l,env)
            func_l = self.heap.get(func_l_index)
            obj_l = self.heap.get(func_l.attributes["partial_args"][0])
            bool_l = func_l.attributes["body"][0](obj_l)
            left_vt = obj_l.version_table
        except NameError as e:
            bool_l = True
            left_vt = VersionTable("None", 0, False).empty()
        
        if bool_l and isinstance(op, Or):
            obj_true.version_table.append(left_vt)
            result_index = self.heap.allocate(obj_true)
            return result_index
        elif (not bool_l) and isinstance(op, And):
            obj_false.version_table.append(left_vt)
            result_index = self.heap.allocate(obj_false)
            return result_index
        
        # rightのbool値の計算
        # NoneもTrueになってしまう
        try:
            func_r_index = self.interpret(node_r,env)
            func_r = self.heap.get(func_r_index)
            obj_r = self.heap.get(func_r.attributes["partial_args"][0])
            bool_r = func_r.attributes["body"][0](obj_r)
            right_vt = obj_r.version_table
        except NameError as e:
            bool_r = True
            left_vt = VersionTable("None", 0, False).empty()
        
        # バージョン検査
        checkCompatibility(left_vt, right_vt)
        
        if bool_r:
            obj_true.version_table.append(left_vt)
            obj_true.version_table.append(right_vt)
            result_index = self.heap.allocate(obj_true)
            return result_index
        else:
            obj_false.version_table.append(right_vt)
            obj_false.version_table.append(left_vt)
            result_index = self.heap.allocate(obj_false)
            return result_index

    # 単項演算子(現在はnotのみ)の評価
    def interpret_UnaryOp(self, node, env):
        op = node.op
        attr = node.value

        obj_true = VObject("bool", VersionTable("bool", 0, False), value=True)
        obj_false = VObject("bool", VersionTable("bool", 0, False), value=False)

        # NoneもTrueになってしまう
        try:
            func_index = self.interpret(attr,env)
            func_obj = self.heap.get(func_index)
            original_obj = self.heap.get(func_obj.attributes["partial_args"][0])
            original_obj_bool = func_obj.attributes["body"][0](original_obj)
            original_obj_vt = original_obj.version_table
        except NameError as e:
            original_obj_bool = True
            original_obj_vt = VersionTable("None", 0, False).empty()

        if not original_obj_bool:
            obj_true.version_table.append(original_obj_vt)
            result_index = self.heap.allocate(obj_true)
            return result_index
        else:
            obj_false.version_table.append(original_obj_vt)
            result_index = self.heap.allocate(obj_false)
            return result_index

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
        if(node.value is not None):
            # リターン文は引数の式の評価結果をそのまま返す
            return self.interpret(node.value, env)
        else:
            return self.none_index

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
        # incompatibleが呼ばれたオブジェクトの評価
        result_index = self.interpret(node.value, env)
        result_object = self.heap.get(result_index)
        # incompatibleが呼ばれた引数からclassとversionを取得。
        # バージョンはNumberとして保存されている。<-改善した方がいい？
        c = node.args[0].id
        v = int(node.args[1].args[0])
        #VTの書き換え
        result_object.version_table.insert(c, v, True)
        #ヒープに再代入
        self.heap.insert(result_object, result_index)

        return result_index
        left_obj=callable_obj.attributes["value"]
        op = callable_obj.attributes["operator"]

        # operatorによる条件分岐
            # operatorが渡されるobjectの型によって振る舞いが変わることはないため
        ops_for_num = {"+", "-", "*", "/", "%", "//"}
        ops_for_bool = {"&", "|"}

        if op in ops_for_num:
            right_obj_index = self.interpret(arg_node)
            right_obj = self.heap.get(right_obj_index)
            if((left_obj.type_tag != "number") & (right_obj.type_tag != "number")):
                raise TypeError(f"The operator {op} is defined for number values")
            ans_type = "number"

            match op:
                case "*":
                    ans_val = left_obj.attributes["value"] * right_obj.attributes["value"]
                case "/":
                    ans_val = left_obj.attributes["value"] / right_obj.attributes["value"]
                case "+":
                    ans_val = left_obj.attributes["value"] + right_obj.attributes["value"]
                case "-":
                    ans_val = left_obj.attributes["value"] - right_obj.attributes["value"]
                case "%":
                    ans_val = left_obj.attributes["value"] % right_obj.attributes["value"]
                case "//":
                    ans_val = left_obj.attributes["value"] // right_obj.attributes["value"]
                case _:
                    raise TypeError("undefined operator")
        elif op in ops_for_bool:
            if((left_obj.type_tag != "bool")):
                raise TypeError(f"The operator {op} is defined for boolean values")
            ans_type = "bool"

            match op:
                case "&":
                    if(not left_obj.attributes["value"]):
                        ans_val = False
                        # 互換性検査で用いるright_objのダミー
                        tmp_vt = VersionTable("None", 0, False)
                        tmp_vt.empty()
                        right_obj = VObject("", tmp_vt)
                    else:
                        right_obj_index = self.interpret(arg_node)
                        right_obj = self.heap.get(right_obj_index)
                        ans_val = right_obj.attributes["value"]
                case "|":
                    if(left_obj.attributes["value"]):
                        ans_val = True
                        # 互換性検査で用いるright_objのダミー
                        tmp_vt = VersionTable("None", 0, False)
                        tmp_vt.empty()
                        right_obj = VObject("", tmp_vt)
                    else:
                        right_obj_index = self.interpret(arg_node)
                        right_obj = self.heap.get(right_obj_index)
                        ans_val = right_obj.attributes["value"]
                case _:
                    raise TypeError("undefined operator")
        elif(isinstance(op, CompOp)):
            right_obj_index = self.interpret(arg_node)
            right_obj = self.heap.get(right_obj_index)
            ans_type = "bool"

            match op.op:
                case "==":
                    ans_val = left_obj.attributes["value"] == right_obj.attributes["value"]
                case "!=":
                    ans_val = left_obj.attributes["value"] != right_obj.attributes["value"]
                case ">":
                    ans_val = left_obj.attributes["value"] > right_obj.attributes["value"]
                case "<":
                    ans_val = left_obj.attributes["value"] < right_obj.attributes["value"]
                case "<=":
                    ans_val = left_obj.attributes["value"] <= right_obj.attributes["value"]
                case ">=":
                    ans_val = left_obj.attributes["value"] >= right_obj.attributes["value"]
                case _:
                    raise TypeError("undefined operator")
            

                
        #互換性検査
        checkCompatibility(left_obj.version_table, right_obj.version_table)
        obj_vt = VersionTable("None", 0, False)
        obj_vt.vt = []
        obj_vt.append(left_obj.version_table)
        obj_vt.append(right_obj.version_table)
        
        obj = VObject(ans_type, obj_vt, value=ans_val)
        obj_index = self.heap.allocate(obj)
        return obj_index

