class VersionError(Exception):
    def __init__(self, message):
        self.message = message

# どのクラスのどのバージョンについてエラーが発生したかを自動で出力する仕組みは未実装
# 現在は、上流の開発者が指定するfeedbackに、それを依存している。

def _feedback_join(*args):
    result = []
    for arg in args:
        if hasattr(arg, "_error_feedbacks"):
            result += arg._error_feedbacks
    return result

def _issue_warning(*args):
    print("-- Version Inconsistency Error --")
    print("Incompatible version usage found in Line ~~ :")
    feedbacks = _feedback_join(*args)
    for feedback in feedbacks:
        print(f"    {feedback}\n")
    print("---------------------------------")

# -------------
# VT Operations
# -------------

# def _vt_well_fromed(obj):
#     if hasattr(obj, "vt"):
#         vt = obj.vt
#         return ((((vt >> 1) & vt) >> 1) | ((vt >> 3) & vt)) & check_bit_mask == 0
#     return True

# def _vt_join(target, *args):
#     tmp_vt = 0
#     if hasattr(target, "vt"):
#         tmp_vt = tmp_vt | target.vt
#     for arg in args:
#         if hasattr(arg, "vt"):
#             tmp_vt = tmp_vt | arg.vt
#     if tmp_vt != 0:
#         target.vt = tmp_vt
#     return target

def _vt_join(vt1, vt2):
    return vt1 | vt2

def _vt_well_formed(vt):
    return ((((vt >> 1) & vt) >> 1) | ((vt >> 3) & vt)) & check_bit_mask == 0

# -------------
# Decorators & Pre-defined functions
# -------------

# for declaring incompatibility
def _incompatible_value(self, _class, _version, _feedback):
    if not hasattr(self, "vt"):
        self.vt = 0
    version_list = limited_classes[str(_class)][1]
    if version_list[0] == str(_version):
        n = limited_classes[str(_class)][0] * 4 + 1
    else:
        n = limited_classes[str(_class)][0] * 4 + 3
    mask = 0b11 << (n-1)    
    self.vt = self.vt | mask

    self._error_feedbacks = [_feedback]
    return self

# for normal method
def _vt_invk(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is not None:
            result.vt = _vt_join(result.vt, args[0].vt)
            if not _vt_well_formed(result.vt):
                _issue_warning(result, args[0])
        return result
    return wrapper

# for literals' method
def _vt_builtin_op(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is not None:
                for arg in args:
                    result.vt = _vt_join(result.vt, arg.vt)
                for kwarg in kwargs:
                    result.vt = _vt_join(result.vt, kwarg.vt)
                if not _vt_well_formed(result.vt):
                    _issue_warning(result, *args, **kwargs)
            return result
        except:
            # Pythonからのエラーで落ちるとき、Versionのconsistencyを先に検査する
            tmp_vt = 0
            for arg in args:
                tmp_vt = _vt_join(tmp_vt, arg.vt)
            for kwarg in kwargs:
                tmp_vt = _vt_join(tmp_vt, kwarg.vt)  
            if not _vt_well_formed(tmp_vt):
                _issue_warning(*args, **kwargs)
            # Pythonのエラーを出すために再度問題のある計算を行う
            result = func(*args, **kwargs)
            # 仮に問題が出なかったら次に進む
            return result
    return wrapper

# for field reference
def _vt_field(receiver, result):
    result.vt = _vt_join(result.vt, receiver.vt)
    if not _vt_well_formed(result.vt):
                _issue_warning(result, receiver)
    return result

# -------------
# Dispatcher
# -------------
def _wrap_primitive(value):
    match type(value):
        case int(): result = VInt(value)
        case float(): result = VFloat(value)
        case str(): result = VStr(value)
        case bool(): result = VBool(value)
        case list(): result = VList(value)
        case _: result = value
    return result

# -------------
# For Debug
# -------------
def _print_vt(value):
    if hasattr(value, "vt"):
        print(f"value {value} has vt: {value.vt}")
    else:
        print(f"value {value} has no vt")
    return
