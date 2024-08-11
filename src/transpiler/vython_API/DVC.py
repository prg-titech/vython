import re

class VersionError(Exception):
    def __init__(self, message):
        self.message = message

def _checkCompatibility(v1, v2):

    if not (hasattr(v1, "vt") and hasattr(v2, "vt")):
        return
    
    if ((v1.vt >> 1) & (v2.vt >> 2) & check_bit_mask) != 0:
        raise VersionError(f"Incompatible!!")
    
    if ((v1.vt >> 2) & (v2.vt >> 1) & check_bit_mask) != 0:
        raise VersionError(f"Incompatible!!")

    if ((v1.vt) & (v2.vt >> 3) & check_bit_mask) != 0:
        raise VersionError(f"Incompatible!!")
    
    if ((v1.vt >> 3) & (v2.vt) & check_bit_mask) != 0:
        raise VersionError(f"Incompatible!!")

    return

def _checkCompatibilities(*args):

    num_args = len(args)

    for i in range(num_args-1):
        for j in range(1, num_args-i):
            _checkCompatibility(args[i], args[i+j])               
    
    return

def _vt_concatenate(target, value):
    if hasattr(value, "vt"):
        target.vt = target.vt | value.vt
    return target

def _vt_concatenate_all(target, *args):
    if not hasattr(target, "vt"):
        target.vt = 0
    for arg in args:
        _vt_concatenate(target, arg)
    return target

def _incompatible_value(self, _class, _version):
    if not hasattr(self, "vt"):
        self.vt = 0
    version_list = limited_classes[str(_class)][1]
    if version_list[0] == str(_version):
        n = limited_classes[str(_class)][0] * 4 + 1
    else:
        n = limited_classes[str(_class)][0] * 4 + 3
    mask = 1 << n    
    self.vt = self.vt | mask
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
