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

def get_set_bit_positions(bit_string):
    positions = []
    position = 0

    while bit_string > 0:
        # ビット列の最下位ビットが1かどうかをチェック
        if bit_string & 1:
            positions.append(position)
        # 次のビットに移動
        bit_string >>= 1
        position += 1

    return positions


def _checkCompatibility(v1, v2):
    # if not (hasattr(v1, "vt") and hasattr(v2, "vt")):
    #     return
    
    # for x in v1.vt:
    #     if x[2]:
    #         c = x[0]
    #         v = x[1]
    #         for y in v2.vt:
    #             if((y[0]==c) and (y[1]!=v)):
    #                 raise TypeError(f"Inconsistent Version Usage:\nComparing {c}!{v} and {c}!{y[1]} values")
    # for y in v2.vt:
    #     if(y[2]):
    #         c = y[0]
    #         v = y[1]
    #         for x in v1.vt:
    #             if((x[0]==c) and (x[1]!=v)):
    #                 raise TypeError(f"Inconsistent Version Usage:\nComparing {c}!{x[1]} and {c}!{v} values")

    if not (hasattr(v1, "vt") and hasattr(v2, "vt")):
        return
    
    if (v1.vt & incompatible_bit) != 0:
        positions = get_set_bit_positions(v1.vt & incompatible_bit)
        for position in positions:
            position = (position - 1) / 2 - 4
            incompatible_list = classes_bit_dict[position]
            incompatible_vt = 0
            for i in incompatible_list:
                n = (i + 4) * 2
                mask = 0b11 << n
                incompatible_vt = incompatible_vt | mask
            if (incompatible_vt & v2.vt) != 0:
                raise TypeError(f"Incompatible!")
    
    if (v2.vt & incompatible_bit) != 0:
        positions = get_set_bit_positions(v2.vt & incompatible_bit)
        for position in positions:
            position = (position - 1) / 2 - 4 
            incompatible_list = classes_bit_dict[position]
            incompatible_vt = 0
            for i in incompatible_list:
                n = (i + 4) * 2
                mask = 0b11 << n
                incompatible_vt = incompatible_vt | mask
            if (incompatible_vt & v1.vt) != 0:
                raise TypeError(f"Incompatible!")    
    return

def _checkCompatibilities(*args):

    num_args = len(args)

    for i in range(num_args-1):
        for j in range(num_args-i):
            _checkCompatibility(args[i], args[i+j])               
    
    return

# 使わなくなった
# def _vt_initialize(self):
#     self.vt = []
#     cv_pair = _extract_class_version(self)
#     self.vt.append((cv_pair[0],cv_pair[1],False))

#     return self

def _vt_concatenate(target, value):
    # 重複を消してない
    if hasattr(value, "vt"):
        # for x in value.vt:
        #     target.vt.append(x)
        target.vt = target.vt | value.vt
    return target

def _vt_concatenate_all(target, *args):
    if not hasattr(target, "vt"):
        target.vt = []
    for arg in args:
        _vt_concatenate(target, arg)
    return target

def _incompatible_value(self, _class, _version):
    if not hasattr(self, "vt"):
        self.vt = 0
    n = (collect_classes_dict[(str(_class), str(_version))] + 4) * 2 + 1
    mask = 1 << n    
    self.vt = self.vt | mask
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
def _vt_concat_decorator_user(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        result = _vt_concatenate_all(result, args[0])
        return result
    return wrapper

# for primitive
def _vt_concat_decorator_primitive(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        result = _vt_concatenate_all(result, *args, **kwargs)
        return result
    return wrapper

def _vt_check_decorator(func):
    def wrapper(*args, **kwargs):
        _checkCompatibilities(*args, **kwargs)
        result = func(*args, **kwargs)
        return result
    return wrapper
