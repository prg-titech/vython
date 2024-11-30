import re

class VersionError(Exception):
    def __init__(self, message):
        self.message = message

def generate_feedback(obj):     
    # エラー発生箇所についてフィードバックを生成
    feedback = ""
    if hasattr(obj, "_error_feedback"):
        for error_feedback in obj._error_feedbacks:
            feedback += error_feedback
            feedback += "\n"
    return feedback

# -------------
# VT Operations
# -------------

def _vt_well_fromed(obj):
    if hasattr(obj, "vt"):
        vt = obj.vt
        if ((((vt >> 1) & vt) >> 1) | ((vt >> 3) & vt)) & check_bit_mask != 0:
            feedback = generate_feedback(obj)
            raise VersionError(f"{feedback}")               
    return

def _vt_join(target, *args):
    tmp_vt = 0
    if hasattr(target, "vt"):
        tmp_vt = tmp_vt | target.vt
    for arg in args:
        if hasattr(arg, "vt"):
            tmp_vt = tmp_vt | arg.vt
    if tmp_vt != 0:
        target.vt = tmp_vt
    return target

# -------------
# Decorators & Pre-defined functions
# -------------

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

    self._error_feedbacks = [_feedback]
    return self

# for user defined method
def _vt_invk(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is not None:
            result = _vt_join(result, args[0])
            _vt_well_fromed(result)
        return result
    return wrapper

# for primitive
def _vt_builtin_op(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is not None:
            result = _vt_join(result, *args, **kwargs)
            _vt_well_fromed(result)
        return result
    return wrapper
