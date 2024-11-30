import numbers

# @_vt_builtin_op を自明でないものにもつけてる

class VInt(int):

    def __init__(self, value):
        self._value = value
        
    # 抽象プロパティ
    # @property
    # def real(self) -> int: ...
    # @property
    # def imag(self) -> Literal[0]: ...
    # @property
    # def numerator(self) -> int: ...
    # @property
    # def denominator(self) -> Literal[1]: ...
    # def conjugate(self) -> int: ...
    # def bit_length(self) -> int: ...

    
    @_vt_builtin_op
    def __add__(self, value):
        return VInt(super().__add__(value))
    
    @_vt_builtin_op
    def __sub__(self, value):
        return VInt(super().__sub__(value))
    
    @_vt_builtin_op
    def __mul__(self, value):
        return VInt(super().__mul__(value))
    
    @_vt_builtin_op
    def __floordiv__(self, value):
        return VInt(super().__floordiv__(value))
    
    @_vt_builtin_op
    def __truediv__(self, value):
        return VFloat(super().__truediv__(value))
    
    @_vt_builtin_op
    def __mod__(self, value):
        return VInt(super().__mod__(value))
    
    @_vt_builtin_op
    def __divmod__(self, value):
        return (VInt(super().__divmod__(value)[0]), VInt(super().__divmod__(value)[1]))
    
    @_vt_builtin_op
    def __radd__(self, value):
        return VInt(super().__radd__(value))
    
    @_vt_builtin_op
    def __rsub__(self, value):
        return VInt(super().__rsub__(value))
    
    @_vt_builtin_op
    def __rmul__(self, value):
        return VInt(super().__rmul__(value))
    
    @_vt_builtin_op
    def __rfloordiv__(self, value):
        return VInt(super().__rfloordiv__(value))
    
    @_vt_builtin_op
    def __rtruediv__(self, value):
        return VFloat(super().__rtruediv__(value))
    
    @_vt_builtin_op
    def __rmod__(self, value):
        return VInt(super().__rmod__(value))
    
    @_vt_builtin_op
    def __rdivmod__(self, value):
        return (VInt(super().__rdivmod__(value)[0]), VInt(super().__rdivmod__(value)[1]))
    
    # ------------------
    # __pow__ の実装は複雑そう？
    # class int の定義を見て後で実装
    # ------------------

    # def __pow__(...):
    #     ...
    # def __rpow__(...):
    #     ...

    
    @_vt_builtin_op
    def __and__(self, value):
        return VInt(super().__and__(value))
    
    @_vt_builtin_op
    def __or__(self, value):
        return VInt(super().__or__(value))
    
    @_vt_builtin_op
    def __xor__(self, value):
        return VInt(super().__xor__(value))
    
    @_vt_builtin_op
    def __lshift__(self, value):
        return VInt(super().__lshift__(value))
    
    @_vt_builtin_op
    def __rshift__(self, value):
        return VInt(super().__rshift__(value))
    
    @_vt_builtin_op
    def __rand__(self, value):
        return VInt(super().__rand__(value))
    
    @_vt_builtin_op
    def __ror__(self, value):
        return VInt(super().__ror__(value))
    
    @_vt_builtin_op
    def __rxor__(self, value):
        return VInt(super().__rxor__(value))
    
    @_vt_builtin_op
    def __rlshift__(self, value):
        return VInt(super().__rlshift__(value))
    
    @_vt_builtin_op
    def __rrshift__(self, value):
        return VInt(super().__rrshift__(value))
    
    def __neg__(self):
        return VInt(super().__neg__())
    def __pos__(self):
        return VInt(super().__pos__())
    def __invert__(self):
        return VInt(super().__invert__())
    def __trunc__(self):
        return VInt(super().__trunc__())
    def __ceil__(self):
        return VInt(super().__ceil__())
    def __floor__(self):
        return VInt(super().__floor__())
    
    # def __round__(...):
    #     ...

    def __getnewargs__(self):
        return (VInt(super().__getnewargs__(self)))
    
    
    @_vt_builtin_op
    def __eq__(self, value):
        return VBool(super().__eq__(value))
    
    @_vt_builtin_op
    def __ne__(self, value):
        return VBool(super().__ne__(value))
    
    @_vt_builtin_op
    def __lt__(self, value):
        return VBool(super().__lt__(value))
    
    @_vt_builtin_op
    def __le__(self, value):
        return VBool(super().__le__(value))
    
    @_vt_builtin_op
    def __gt__(self, value):
        return VBool(super().__gt__(value))
    
    @_vt_builtin_op
    def __ge__(self, value):
        return VBool(super().__ge__(value))
    
    def __float__(self):
        return VFloat(super().__float__())
    def __int__(self):
        return VInt(super().__int__())
    def __abs__(self):
        return VInt(super().__abs__())
    def __hash__(self):
        return VInt(super().__hash__())
    def __bool__(self):
        return VBool(super().__bool__())
    def __index__(self):
        return VInt(super().__index__())

class VFloat(numbers.Real):

    def __init__(self, value):
        self._value = value

    def __repr__(self) -> str:
        return self._value.__repr__()

    
    # 色々省略している実装がある -> float
    
    
    @_vt_builtin_op
    def __add__(self, value):
        return VFloat(super().__add__(value))
    
    @_vt_builtin_op
    def __sub__(self, value):
        return VFloat(super().__sub__(value))
    
    @_vt_builtin_op
    def __mul__(self, value):
        return VFloat(super().__mul__(value))
    
    @_vt_builtin_op
    def __floordiv__(self, value):
        return VFloat(super().__floordiv__(value))
    
    @_vt_builtin_op
    def __truediv__(self, value):
        return VFloat(super().__truediv__(value))
    
    @_vt_builtin_op
    def __mod__(self, value):
        return VFloat(super().__mod__(value))
    
    @_vt_builtin_op
    def __divmod__(self, value):
        return (VFloat(super().__divmod__(value)[0]), VFloat(super().__divmod__(value)[1]))
    
    
    @_vt_builtin_op
    def __radd__(self, value):
        return VFloat(super().__radd__(value))
    
    @_vt_builtin_op
    def __rsub__(self, value):
        return VFloat(super().__rsub__(value))
    
    @_vt_builtin_op
    def __rmul__(self, value):
        return VFloat(super().__rmul__(value))
    
    @_vt_builtin_op
    def __rfloordiv__(self, value):
        return VFloat(super().__rfloordiv__(value))
    
    @_vt_builtin_op
    def __rtruediv__(self, value):
        return VFloat(super().__rtruediv__(value))
    
    @_vt_builtin_op
    def __rmod__(self, value):
        return VFloat(super().__rmod__(value))
    
    @_vt_builtin_op
    def __rdivmod__(self, value):
        return (VFloat(super().__rdivmod__(value)[0]), VFloat(super().__rdivmod__(value)[1]))
    
    
    @_vt_builtin_op
    def __pow__(self, exponent):
        return VFloat(super().__pow__(exponent))
    
    @_vt_builtin_op
    def __rpow__(self, exponent):
        return VFloat(super().__rpow__(exponent))
    
    def __trunc__(self):
        return VFloat(super().__trunc__())
    def __getnewargs__(self):
        return (VFloat(super().__getnewargs__(self)))
    
    
    @_vt_builtin_op
    def __eq__(self, value):
        return VBool(super().__eq__(value))
    
    @_vt_builtin_op
    def __ne__(self, value):
        return VBool(super().__ne__(value))
    
    @_vt_builtin_op
    def __lt__(self, value):
        return VBool(super().__lt__(value))
    
    @_vt_builtin_op
    def __le__(self, value):
        return VBool(super().__le__(value))
    
    @_vt_builtin_op
    def __gt__(self, value):
        return VBool(super().__gt__(value))
    
    @_vt_builtin_op
    def __ge__(self, value):
        return VBool(super().__ge__(value))

    def __neg__(self):
        return VFloat(super().__neg__())
    def __pos__(self):
        return VFloat(super().__pos__())
    def __ceil__(self):
        return VInt(super().__ceil__())
    def __floor__(self):
        return VInt(super().__floor__())
    def __round__(self, ndigit=None):
        return VFloat(super().__round__(ndigit))
        

    def __float__(self):
        return VFloat(super().__float__())
    def __int__(self):
        return VInt(super().__int__())
    def __abs__(self):
        return VFloat(super().__abs__())
    def __hash__(self):
        return VInt(super().__hash__())
    def __bool__(self):
        return VBool(super().__bool__())

class VBool(int):

    def __init__(self, value):
        self._value = value

    def __repr__(self):
        if self._value == 1:
            return f"{True}"
        else:
            return f"{False}"

    
    # Pythonでboolはintの派生クラス
    

    # 次の6つのメソッドは厳密には違う実装をしている。
    # Pythonではvalueの型がintかboolかによって返り値の型が変化

    
    @_vt_builtin_op
    def __and__(self, value):
        return VInt(super().__and__(value))
    
    @_vt_builtin_op
    def __or__(self, value):
        return VInt(super().__or__(value))
    
    @_vt_builtin_op
    def __xor__(self, value):
        return VInt(super().__xor__(value))
    
    @_vt_builtin_op
    def __rand__(self, value):
        return VInt(super().__rand__(value))
    
    @_vt_builtin_op
    def __ror__(self, value):
        return VInt(super().__ror__(value))
    
    @_vt_builtin_op
    def __rxor__(self, value):
        return VInt(super().__rxor__(value))
    
    def __invert__(self):
        return VInt(super().__invert__())
    def __getnewargs__(self):
        return (VInt(super().__getnewargs__(self)))

class VStr(str):

    def __init__(self, value):
        self._value = value

    
    # 後で諸々は実装
    