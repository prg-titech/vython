class Primitive_String_v_0():
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"
    
    def __bool__(self):
        return bool(self.value)
    
    def __len__(self):
        return len(self.value)
    
    def equal(left,right):
        return left.value == right.value
    def nequal(left,right):
        return left.value != right.value
    
    def __add__(left,right):
        return left.binary(right,"add")
    def __eq__(left,right):
        return left.binary(right,"eq")
    def __ne__(left,right):
        return left.binary(right,"ne")
    def __lt__(left,right):
        return left.binary(right,"lt")
    def __gt__(left,right):
        return left.binary(right,"gt")
    def __le__(left,right):
        return left.binary(right,"le")
    def __ge__(left,right):
        return left.binary(right,"ge")
    
    def binary(left,right,op):
        match op:
            # 連結
            case "add": result = Primitive_String_v_0(left.value + right.value)
            # 比較
            case "eq": result = Primitive_Bool_v_0(left.value == right.value)
            case "ne": result = Primitive_Bool_v_0(left.value != right.value)
            case "lt": result = Primitive_Bool_v_0(left.value < right.value)
            case "gt": result = Primitive_Bool_v_0(left.value > right.value)
            case "le": result = Primitive_Bool_v_0(left.value <= right.value)
            case "ge": result = Primitive_Bool_v_0(left.value >= right.value)
        return result
