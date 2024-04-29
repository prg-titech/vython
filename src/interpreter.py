from src.syntax.semantics import *
from src.syntax.language import *
from src.compatibilitychecker import *
from src.specialclasses import *
import copy


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
        func_obj = VObject("function", VersionTable("NormalFunction", 0, False), name=function_name, args=arg_names, body=node.body)

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
        func_obj = VObject("function", VersionTable(c, v, False), name=function_name, args=arg_names, body=node.body)

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
    
    # TruthyかFalthyかを分類し、True,Falseに変換
    def interpret_Boolean(self, node, env):
        obj_index = self.interpret(node.value)
        obj = self.heap.get(obj_index)

        # objがTruthyかFalthyかの分類
        if((obj.type_tag=="bool") | (obj.type_tag=="number") | (obj.type_tag=="string")):
            if(obj.attributes["value"]):
                return self.interpret_ConstTrue(node, env)
            else:
                return self.interpret_ConstFalse(node, env)
        elif(obj.type_tag=="None"):
            return self.interpret_ConstFalse(node, env)
        else:
            return self.interpret_ConstTrue(node, env)
            
    # 真偽値の評価
    def interpret_ConstTrue(self, node, env):
        obj_vt = VersionTable("Bool", 0, False)
        obj_vt.empty()
        obj = VObject("bool", obj_vt, value=True)
        obj_index = self.heap.allocate(obj)
        return obj_index
    
    def interpret_ConstFalse(self, node, env):
        obj_vt = VersionTable("Bool", 0, False)
        obj_vt.empty()
        obj = VObject("bool", obj_vt, value=False)
        obj_index = self.heap.allocate(obj)
        return obj_index
    
    # 数値の評価
    def interpret_Number(self, node, env):
        obj_vt = VersionTable("Number", 0, False)
        obj_vt.empty()
        obj = VObject("number", obj_vt, value=float(node.number))
        obj_index = self.heap.allocate(obj)
        return obj_index

    # 文字列の評価
    def interpret_String(self, node, env):
        obj_vt = VersionTable("String", 0, False)
        obj_vt.empty()
        obj = VObject("string", obj_vt, value=node.string)
        obj_index = self.heap.allocate(obj)
        return obj_index
    
    # # 比較式の評価
    # def interpret_Comparison(self, node, env):
    #     comp_list_length = len(node.comp_list)
    #     # CompOpの数
    #     comp_op_size = int((comp_list_length - 1) / 2)
    #     # 比較されるオブジェクトを評価
    #     interpreted_obj_index_list = []
    #     for i in range(comp_op_size + 1):
    #         obj_2i = self.interpret(node.comp_list[2*i], env)
    #         interpreted_obj_index_list.append(obj_2i)

    #     # 比較演算
    #     compared_obj_list = []
    #     for i in range(comp_op_size):
    #         comp_op = node.comp_list[2*i+1]
    #         obj_left_index = interpreted_obj_index_list[i]
    #         obj_right_index = interpreted_obj_index_list[i+1]
    #         obj_left = self.heap.get(obj_left_index)
    #         obj_right = self.heap.get(obj_right_index)

    #         #互換性検査
    #         checkCompatibility(obj_left.version_table, obj_right.version_table)
    #         obj_i_vt = VersionTable("None", 0, False)
    #         obj_i_vt.vt = []
    #         obj_i_vt.append(obj_left.version_table)
    #         obj_i_vt.append(obj_right.version_table)
            
    #         match comp_op.op:
    #             case "==":
    #                 b = obj_left.attributes["value"] == obj_right.attributes["value"]
    #             case "!=":
    #                 b = obj_left.attributes["value"] != obj_right.attributes["value"]
    #             case ">":
    #                 b = obj_left.attributes["value"] > obj_right.attributes["value"]
    #             case "<":
    #                 b = obj_left.attributes["value"] < obj_right.attributes["value"]
    #             case "<=":
    #                 b = obj_left.attributes["value"] <= obj_right.attributes["value"]
    #             case ">=":
    #                 b = obj_left.attributes["value"] >= obj_right.attributes["value"]
    #             case _:
    #                 raise TypeError("undefined operator")
            
    #         obj_i = VObject("bool", obj_i_vt, value=b)
    #         compared_obj_list.append(obj_i)

    #     # compared_obj_listが1以上なら各要素を&で結合
    #     obj = compared_obj_list[0]
    #     if(len(compared_obj_list) > 1):
    #         for i in range(len(compared_obj_list) - 1):
    #             obj_right = compared_obj_list[i+1]

    #             #互換性検査
    #             checkCompatibility(obj.version_table, obj_right.version_table)
    #             obj_i_vt = VersionTable("None", 0, False)
    #             obj_i_vt.vt = []
    #             obj_i_vt.append(obj.version_table)
    #             obj_i_vt.append(obj_right.version_table)

    #             b = obj.attributes["value"] & obj_right.attributes["value"]

    #             obj = VObject("bool", obj_i_vt, value=b)

    #     obj_index = self.heap.allocate(obj)
    #     return obj_index
    
    # # or式の評価
    # def interpret_OrExpr(self, node, env):
    #     obj_left_index = self.interpret(node.left, env)
    #     obj_right_index = self.interpret(node.right, env)
    #     obj_left = self.heap.get(obj_left_index)
    #     obj_right = self.heap.get(obj_right_index)

    #     # obj_left,rightがBoolかNumberかの確認
    #     lt = obj_left.type_tag
    #     rt = obj_right.type_tag
    #     _boolean = {"number", "bool"}
    #     if((lt in _boolean) & (rt in _boolean)):
    #         pass
    #     else:
    #         raise TypeError("boolean value is required in OrExpr")
        
    #     #互換性検査
    #     checkCompatibility(obj_left.version_table, obj_right.version_table)
    #     obj_vt = VersionTable("None", 0, False)
    #     obj_vt.vt = []
    #     obj_vt.append(obj_left.version_table)
    #     obj_vt.append(obj_right.version_table)
        
    #     # ASTからPythonのTrue,False値に落とす
    #     match lt:
    #         case "number":
    #             lb = (obj_left.attributes["value"] != 0)
    #         case "bool":
    #             lb = obj_left.attributes["value"]
    #     match rt:
    #         case "number":
    #             rb = (obj_right.attributes["value"] != 0)
    #         case "bool":
    #             rb = obj_right.attributes["value"]

    #     # lb | rb を計算し、ヒープに配置、インデックスを返す
    #     b = lb | rb
    #     obj = obj = VObject("bool", obj_vt, value=b)
    #     obj_index = self.heap.allocate(obj)
    #     return obj_index

    # # and式の評価
    # def interpret_AndExpr(self, node, env):
        obj_left_index = self.interpret(node.left, env)
        obj_right_index = self.interpret(node.right, env)
        obj_left = self.heap.get(obj_left_index)
        obj_right = self.heap.get(obj_right_index)

        # obj_left,rightがBoolかNumberかの確認
        lt = obj_left.type_tag
        rt = obj_right.type_tag
        _boolean = {"number", "bool"}
        if((lt in _boolean) & (rt in _boolean)):
            pass
        else:
            raise TypeError("boolean value is required in AndExpr")
        
        #互換性検査
        checkCompatibility(obj_left.version_table, obj_right.version_table)
        obj_vt = VersionTable("None", 0, False)
        obj_vt.empty()
        obj_vt.append(obj_left.version_table)
        obj_vt.append(obj_right.version_table)
        
        # ASTからPythonのTrue,False値に落とす
        match lt:
            case "number":
                lb = (obj_left.attributes["value"] != 0)
            case "bool":
                lb = obj_left.attributes["value"]
        match rt:
            case "number":
                rb = (obj_right.attributes["value"] != 0)
            case "bool":
                rb = obj_right.attributes["value"]

        # lb & rb を計算し、ヒープに配置、インデックスを返す
        b = lb & rb
        obj = VObject("bool", obj_vt, value=b)
        obj_index = self.heap.allocate(obj)
        return obj_index
    
    # # 数値演算の評価
    # def interpret_ArithExpr(self, node, env):
    #     obj_left_index = self.interpret(node.left, env)
    #     obj_right_index = self.interpret(node.right, env)
    #     obj_left = self.heap.get(obj_left_index)
    #     obj_right = self.heap.get(obj_right_index)
    #     op = node.op

    #     # obj_left,rightがNumberかの確認
    #     if((obj_left.type_tag != "number") & (obj_right.type_tag != "number")):
    #         raise TypeError("number is required in ArithExpr")

    #     match op:
    #         case "+":
    #             n = obj_left.attributes["value"] + obj_right.attributes["value"]
    #         case "-":
    #             n = obj_left.attributes["value"] - obj_right.attributes["value"]
    #         case _:
    #             raise TypeError("undefined operator")
            
    #     #互換性検査
    #     checkCompatibility(obj_left.version_table, obj_right.version_table)
    #     obj_vt = VersionTable("None", 0, False)
    #     obj_vt.vt = []
    #     obj_vt.append(obj_left.version_table)
    #     obj_vt.append(obj_right.version_table)
        
    #     obj = VObject("number", obj_vt, value=n)
    #     obj_index = self.heap.allocate(obj)
    #     return obj_index

    # # Termの評価
    # def interpret_Term(self, node, env):
        obj_left_index = self.interpret(node.left, env)
        obj_right_index = self.interpret(node.right, env)
        obj_left = self.heap.get(obj_left_index)
        obj_right = self.heap.get(obj_right_index)
        op = node.op

        # obj_left,rightがNumberかの確認
        if((obj_left.type_tag != "number") & (obj_right.type_tag != "number")):
            raise TypeError("number is required in ArithExpr")

        match op:
            case "*":
                n = obj_left.attributes["value"] * obj_right.attributes["value"]
            case "/":
                n = obj_left.attributes["value"] / obj_right.attributes["value"]
            case "%":
                n = obj_left.attributes["value"] % obj_right.attributes["value"]
            case "//":
                n = obj_left.attributes["value"] // obj_right.attributes["value"]
            case _:
                raise TypeError("undefined operator")
        
        #互換性検査
        checkCompatibility(obj_left.version_table, obj_right.version_table)
        obj_vt = VersionTable("None", 0, False)
        obj_vt.empty()
        obj_vt.append(obj_left.version_table)
        obj_vt.append(obj_right.version_table)
        
        obj = VObject("number", obj_vt, value=n)
        obj_index = self.heap.allocate(obj)
        return obj_index
    
    # Factorの評価
    def interpret_Factor(self, node, env):
        obj_value_index = self.interpret(node.value, env)
        obj_value = self.heap.get(obj_value_index)
        op = node.op

        obj_index = obj_value_index

        # valueがNumberでなかったらエラー
        match obj_value.type_tag:
            case "number":
                if(op == "+"):
                    pass
                elif(op == "-"):
                    n = obj_value.attributes["value"]
                    obj = VObject("number", obj_value.version_table, value = (-1) * n)
                    obj_index = self.heap.allocate(obj)
                else:
                    raise TypeError(f"We don't support this Operator: {op}")
            case _:
                raise TypeError("number is required in Factor")
            
        return obj_index
    
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
            instance_attributes = {
                method_name: method_obj
                for method_name, method_obj in callable_obj.attributes["body"].items()
            }

            # インスタンスのクラスとバージョンを環境のクラス定義から得る
            # 本質的でない実装の可能性
            instance_vt = callable_obj.version_table

            # インスタンスオブジェクト作成
            instance = VObject(type_tag, VersionTable(instance_vt.vt[0][0], instance_vt.vt[0][1], False), **instance_attributes)

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

                # メソッド定義の引数リストの深いコピーを作成し、selfを除去
                args_copy = copy.deepcopy(init_method.attributes["args"])
                args_copy.pop(0)

                # 引数を評価し、ローカル環境にセット
                for arg_name, arg_value in zip(
                    args_copy, node.args
                ):
                    if (arg_name is not None):
                        evaluated_arg = self.interpret(arg_value, method_env)
                        method_env.set(arg_name, None, evaluated_arg) # ネストクラスを定義するならこの実装ではマズいかも
                for statement in init_method.attributes["body"]:
                    self.interpret(statement, method_env)

            # オブジェクトが格納されているヒープへのindexを返す
            return heap_index

        # 関数の評価, オブジェクトから属性参照で取り出されたメソッド呼び出しのケースを含む
        elif callable_obj.type_tag == "function":
            # 新しいローカル環境を作成
            local_env = Environment(parent=env)

            # 変数 'self' にインスタンスのインデックスをバインド 
            #### ここでバインドされているのはインスタンスのインデックスではなくインスタンスから呼ばれたfunction 
            # local_env.set("self", None, callable_obj_index)
        
            # 応急処置 heapが汚くなるが再度オブジェクトをメインのヒープ内に作ることにする。しょうがない。
            # 何か問題があるかもしれない
            # 属性参照によるメソッド呼び出しの場合特別にselfとしてバインド
            if type(node.func).__name__ == "Attribute":
                self_index = self.interpret(node.func.value, env)
                local_env.set("self", None, self_index)

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


            # 属性参照によるメソッド呼び出しの場合のVT書き換え操作 & 演算の場合の書き換え操作と互換性検査
            receiver_index = -1
            receiver_vt = VersionTable("None", 0, False)
            receiver_vt.empty()
            receiver_object = VObject("None", receiver_vt)
            if type(node.func).__name__ == "Attribute":
                # レシーバーオブジェクトを取得するために一時的なインタプリタを作成し使用する
                tmpInterpreter = Interpreter()
                tmpInterpreter.heap = self.heap
                tmpInterpreter.global_env = self.global_env
                receiver_index = tmpInterpreter.interpret(node.func.value, env)
                receiver_object = tmpInterpreter.heap.get(receiver_index)
            # 特別なクラスのメソッド呼び出しの場合 => 集合で表現している。
            if callable_obj.version_table.vt[0][0] in special_classes:
                # 引数とレシーバーを取得
                objsForOp_index = list(local_env.bindings.values())
                length = len(objsForOp_index)             
                # 互換性検査
                for i in range(length):
                    vt1 = self.heap.get(objsForOp_index[i]).version_table
                    for j in range(length):
                        vt2 = self.heap.get(objsForOp_index[j]).version_table
                        if (j > i):
                            checkCompatibility(vt1, vt2)
                # 演算での評価結果のVTをレシーバーと引数オブジェクトのVTの結合で上書き(特別なクラスのメソッド呼び出し)
                result_object = self.heap.get(result_index)
                final_result_object_vt = VersionTable("None", 0, False)
                final_result_object_vt.empty()
                for objForOp_index in objsForOp_index:
                    objForOp = self.heap.get(objForOp_index)
                    final_result_object_vt.append(objForOp.version_table)
                result_object.version_table = final_result_object_vt
                # ヒープの同じ場所に代入
                self.heap.insert(result_object, result_index)
            else:
                # 評価結果のオブジェクトのVTにレシーバーオブジェクトのVTを結合(通常のメソッド呼び出し)
                result_object = self.heap.get(result_index)
                result_object.version_table.append(receiver_object.version_table)
                # ヒープの同じ場所に代入
                self.heap.insert(result_object, result_index)
            return result_index
        
        # NumberやStringオブジェクトから呼び出されるメソッド
        elif callable_obj.type_tag == "binary_op":
            # node.argsを評価せずに渡しているのは、and,or演算では評価する必要がない可能性があるため
            result_index = self.calculate_binaryop(callable_obj,node.args)
            return result_index
        
        else:
            # type_tag が "class" でも "function" でもないなら不正な関数呼び出し
            raise TypeError(f"Attribute {callable_obj.type_tag} is not a callable method")

    # 属性参照の評価
    def interpret_Attribute(self, node, env):
        obj_heap_index = self.interpret(node.value, env)

        # ヒープからオブジェクトを取得
        obj = self.heap.get(obj_heap_index)

        #objが特別なクラスのインスタンスであるかを確認
        special_classes = {"number", "bool", "string"}
        if(obj.type_tag in special_classes):
            #バイナリーオペレーションオブジェクトを返す => interpret_callでargsと混ぜて計算
            tmp_vt = VersionTable("None", 0, False).empty()
            binary_op_obj = VObject("binary_op", tmp_vt, value=obj, operator=node.attr)
            binary_op_obj_index = self.heap.allocate(binary_op_obj)
            return binary_op_obj_index

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
        # incompatibleが呼ばれたオブジェクトの評価
        result_index = self.interpret(node.value, env)
        result_object = self.heap.get(result_index)
        # incompatibleが呼ばれた引数からclassとversionを取得。
        # バージョンはNumberとして保存されている。<-改善した方がいい？
        print(node)
        c = node.args[0].id
        v = int(node.args[1].number)
        #VTの書き換え
        result_object.version_table.insert(c, v, True)
        #ヒープに再代入
        self.heap.insert(result_object, result_index)

        return result_index
    
    def calculate_binaryop(self, callable_obj, arg_node):
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


