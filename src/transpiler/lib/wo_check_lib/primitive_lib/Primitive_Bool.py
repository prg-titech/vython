class Primitive_Bool_v_0():
    def __init__(self, value):
        self.value = value
        __vt_init__(self)
    
    def __repr__(self):
        return f"{self.value}"
    
    def __bool__(self):
        return self.value
    
    def equal(left,right):
        return left.value == right.value
    def nequal(left,right):
        return left.value != right.value
    
    # 検査 & VT書き換えを加える
    def __eq__(left,right):
        return left.binary(right,"eq")
    def __ne__(left,right):
        return left.binary(right,"ne")
    
    def binary(left,right,op):
        match op:
            # 比較
            case "eq": result = Primitive_Bool_v_0(left.value == right.value)
            case "ne": result = Primitive_Bool_v_0(left.value != right.value)
        append(result,left)
        append(result,right)
        return result
    