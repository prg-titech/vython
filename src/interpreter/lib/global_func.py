from src.interpreter.syntax.semantics import *
# Python組み込み関数
global_func_list = [
    VObject(type_tag='global_function', 
            version_table=VersionTable('NormalFunction',0,False),
            name = 'print',
            args = ['value'],
            body = [(lambda value: print(value))],
            partial_args = [])
]
