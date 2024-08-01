from lark import Token, Transformer, Tree
import ast
import copy



'''
渡されたvython AST に含まれるクラスとバージョンの情報を収集
'''

# larkToIRを参考に実装する
class CollectClasses(Transformer):
    ############################
    ############################
    # トランスパイラ初期化
    ############################
    ############################
    def __init__(self, debug_mode=None):
        self.debug_mode = debug_mode
        self.collect_classes = set()

    ############################
    ############################
    # module
    ############################
    ############################

    def file_input(self, items):
        return None 


    ############################
    ############################
    # stmt
    ############################
    ############################

    def funcdef(self, items):
        return None

    # + AsyncFunctionDef
    
    def classdef(self, items):
        name, version, bases, body = items[0], items[1], [], self._flatten_list(items[3:])
        # バージョンの情報もクラス名が持つ
        class_name = str(name) + "_v_" + str(version)

        self.collect_classes.add((str(name), str(version)))

        return None
    
    def return_stmt(self, items):
        return None

    # + delete

    def assign_stmt(self, items):
        return None
    
    # TypeAlias

    # AugAssign
    # AnnAssign

    def for_stmt(self, items):
        return None

    # + AsyncFor

    def while_stmt(self, items):
        return None

    def if_stmt(self, items):
        return None
    
    def elifs(self, items):
        return None
    
    def elif_(self, items):
        return None

    # With
    # AsyncWith

    def match_stmt(self, items):
        return None
    
    def case(self, items):
        return None
    
    def literal_pattern(self, items):
        return None
    
    def any_pattern(self, items):
        return None
    
    def or_pattern(self, items):
        return None
    
    # MatchSequence
    # MatchStar
    # MatchMapping
    # MatchClass

    # Raise
    # Try
    # TryStar
    # Assert

    # Import
    # ImportFrom

    # Global
    # NonLocal

    def expr_stmt(self, items):
        return None
    
    def pass_stmt(self, _):
        return None

    def break_stmt(self, items):
        return None

    def continue_stmt(self,items):
        return None


    ############################
    ############################
    # expr
    ############################
    ############################

    # -----------------------------
    # ----- Vython Primitives -----
    # -----------------------------
    def or_test(self, items):
        return None
    
    def and_test(self, items):
        return None

    def not_test(self, items):
        return None
  
    def arith_expr(self, items):
        return None
        
    def term(self, items):
        return None

    def factor(self, items):
        return None

    def lambdef(self, items):
        return None
    
    def lambda_params(self, items):
        return None

    # + IfExp
    # -> lark に対応してなかった

    def dict(self, items):
        return None

    def set(self, items):
        return None
    
    # ListComp
    # SetComp
    # DictComp
    # GeneratorExp

    # Await
    # Yield
    # YieldFrom

    def comparison(self, items):
        return None
    
    def funccall(self, items):
        return None
    
    def funccallwithversion(self, items):
        return None
    
    # FormattedValue
    # JoinedStr
    
    def const_true(self, items):
        return None
    
    def const_false(self, items):
        return None
    
    def string(self, items):
        return None
    
    def number(self, items):
        return None

    def getattr(self, items):
        return None
    
    def getitem(self, items):
        return None

    # Starred

    def name(self, items):
        id = items[0].value
        return str(id)
          
    def var(self, items):
        return None
    
    # List
    def list(self, items):
        return None

    # Tuple
    def tuple(self, items):
        return None

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
        return None
    
    def version(self, items):
        number = items[0]
        return str(number)

    def arguments(self, items):
       return None

    def suite(self, items):
        return None

    def parameters(self, items):
        return None

    # 適切か怪しい
    def const_none(self, _):
        return None

    # _flatten_list メソッドの定義
    def _flatten_list(self, l):
        return None
