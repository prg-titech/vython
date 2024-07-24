import re

def _extract_class_version(self):
    cn = self.__class__.__name__
    # Vython Primitiveの時
    match cn:
        case "VInt": return("VInt","0")
        case "VFloat": return("VFloat","0")
        case "VBool": return("VBool","0")
        case "VStr": return("VStr","0")

    # それ以外の場合、正規表現パターンによる抽出
    # 不正確
    pattern = r'([A-Za-z_0-9]+)_v_([0-9]+)'
    # 正規表現にマッチする部分を検索
    matchRe = re.fullmatch(pattern, cn)
    if matchRe:
        class_name = matchRe[1]  # クラスの名前
        version_number = matchRe[2]  # バージョンの名前
        return (class_name,version_number)
    else:
        raise TypeError("Inappropriate Class Name")

def _checkCompatibility(v1, v2):
    if not (hasattr(v1, "vt") and hasattr(v2, "vt")):
        return
    
    for x in v1.vt:
        if x[2]:
            c = x[0]
            v = x[1]
            for y in v2.vt:
                if((y[0]==c) and (y[1]!=v)):
                    raise TypeError(f"Inconsistent Version Usage:\nComparing {c}!{v} and {c}!{y[1]} values")
    for y in v2.vt:
        if(y[2]):
            c = y[0]
            v = y[1]
            for x in v1.vt:
                if((x[0]==c) and (x[1]!=v)):
                    raise TypeError(f"Inconsistent Version Usage:\nComparing {c}!{x[1]} and {c}!{v} values")
    return

def _checkCompatibilities(*args):
    print("[LOG]: checkCompatibilities() is called")

    num_args = len(args)

    for i in range(num_args-1):
        for j in range(num_args-i):
            _checkCompatibility(args[i], args[i+j])               
    
    print("[LOG]: This is compatible computation")
    return

def _vt_initialize(self):
    self.vt = []
    cv_pair = _extract_class_version(self)
    self.vt.append((cv_pair[0],cv_pair[1],False))
    print(f"[LOG]: Initialized VT with ({cv_pair[0]}, {cv_pair[1]}, {False})")

    return self

def _vt_concatenate(target, value):
    # 重複を消してない
    if hasattr(value, "vt"):
        for x in value.vt:
            target.vt.append(x)
    return target

def _vt_concatenate_all(target, *args):
    if not hasattr(target, "vt"):
        target.vt = []
    for arg in args:
        _vt_concatenate(target, arg)
    return target

def _incompatible_value(self, _class, _version):
    if not hasattr(self, "vt"):
        self.vt = []
    self.vt.append((_class,f"{_version}",True))
    print(f"[LOG]: {self} is incompatible with versions other than {_version} of {_class}")
    return self

# -------------
# Decorators
# -------------
def _vt_init_decorator(func):
    def wrapper(*args, **kwargs):
        _vt_initialize(args[0])
        result = func(*args, **kwargs)
        return result
    return wrapper

# for user defined method
def _vt_concat_decorator1(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[LOG]: Concatenate VT of {args[0]} to VT of {result}")
        result = _vt_concatenate_all(result, args[0])
        return result
    return wrapper

# for primitive
def _vt_concat_decorator2(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[LOG]: Concatenate VT of {args} and {kwargs} to VT of {result}")
        result = _vt_concatenate_all(result, *args, **kwargs)
        return result
    return wrapper

def _vt_check_decorator(func):
    def wrapper(*args, **kwargs):
        _checkCompatibilities(*args, **kwargs)
        result = func(*args, **kwargs)
        return result
    return wrapper
