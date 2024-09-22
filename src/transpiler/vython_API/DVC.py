import re

class VersionError(Exception):
    def __init__(self, message):
        self.message = message

def generate_feedback(*args):
    incompat_tuple_list = []
    # エラー箇所の再特定
    args_size = len(args)
    for i in range(args_size-1):
        for j in range(1, args_size-i):
            v1 = args[i]
            v2 = args[i+j]
            if not (hasattr(v1, "vt") and hasattr(v2, "vt")):
                break
            v1_or_v2 = (v1.vt | v2.vt)
            if ((((v1_or_v2 >> 1) & v1_or_v2) >> 1) | ((v1_or_v2 >> 3) & v1_or_v2)) & check_bit_mask != 0:
                incompat_tuple_list.append((v1, v2))
      
    # エラー発生箇所についてフィードバックを生成
    feedback = ""
    for index, incompat_tuple in enumerate(incompat_tuple_list):
        partial_feedback = f"Version Error {index + 1}:\n"
        if hasattr(v1, "error_feedback"):
            partial_feedback += v1.error_feedback
            partial_feedback += "\n"
        if hasattr(v2, "error_feedback"):
            partial_feedback += v2.error_feedback
            partial_feedback += "\n"
        feedback += partial_feedback
    return feedback

def _checkCompatibilities(*args):
    disjunction_bit = 0
    for arg in args:
        if hasattr(arg, "vt"):
            disjunction_bit = (disjunction_bit | arg.vt)

    if ((((disjunction_bit >> 1) & disjunction_bit) >> 1) | ((disjunction_bit >> 3) & disjunction_bit)) & check_bit_mask != 0:
        feedback = generate_feedback(*args)
        raise VersionError(f"{feedback}")               

    return

def _vt_concatenate_all(target, *args):
    if not hasattr(target, "vt"):
        target.vt = 0
    for arg in args:
        if hasattr(arg, "vt"):
            target.vt = target.vt | arg.vt
    return target

def _incompatible_value(self, _class, _version, _feedback):
    if not hasattr(self, "vt"):
        self.vt = 0
    version_list = limited_classes[str(_class)][1]
    if version_list[0] == str(_version):
        n = limited_classes[str(_class)][0] * 4 + 1
    else:
        n = limited_classes[str(_class)][0] * 4 + 3
    mask = 1 << n    
    self.vt = self.vt | mask

    self.error_feedback = _feedback
    return self

# -------------
# Decorators
# -------------

# for user defined method
def _vt_concat_decorator_user(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is not None:
            result = _vt_concatenate_all(result, args[0])
        return result
    return wrapper

# for primitive
def _vt_concat_decorator_primitive(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is not None:
            result = _vt_concatenate_all(result, *args, **kwargs)
        return result
    return wrapper

def _vt_check_decorator(func):
    def wrapper(*args, **kwargs):
        _checkCompatibilities(*args, **kwargs)
        result = func(*args, **kwargs)
        return result
    return wrapper
