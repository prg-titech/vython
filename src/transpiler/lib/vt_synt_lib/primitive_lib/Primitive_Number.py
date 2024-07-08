class Primitive_Number_v_0():
    def __init__(self, value):
        self.value = value
        __vt_init__(self)
    
    def __repr__(self):
        return f"{self.value}"
    
    def __bool__(self):
        return bool(self.value)
    
    def __str__(self):
        return str(self.value)
    
    def equal(left,right):
        return left.value == right.value
    def nequal(left,right):
        return left.value != right.value

    def __add__(left,right):
        return left.binary(right,"add")
    def __sub__(left,right):
        return left.binary(right,"sub")
    def __mul__(left,right):
        return left.binary(right,"mul")
    def __truediv__(left,right):
        return left.binary(right,"div")
    def __floordiv__(left,right):
        return left.binary(right,"floordiv")
    def __mod__(left,right):
        return left.binary(right,"mod")
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

    def __neg__(self):
        return self.unary("neg")
    def __pos__(self):
        return self.unary("pos")
    
    def binary(left,right,op):
        match op:
            # 算術
            case "add": result = Primitive_Number_v_0(left.value + right.value)
            case "sub": result = Primitive_Number_v_0(left.value - right.value)
            case "mul": result = Primitive_Number_v_0(left.value * right.value)
            case "div": result = Primitive_Number_v_0(left.value / right.value)
            case "mod": result = Primitive_Number_v_0(left.value % right.value)
            case "floordiv": result = Primitive_Number_v_0(left.value // right.value)
            # 比較
            case "eq": result = Primitive_Bool_v_0(left.value == right.value)
            case "ne": result = Primitive_Bool_v_0(left.value != right.value)
            case "lt": result = Primitive_Bool_v_0(left.value < right.value)
            case "gt": result = Primitive_Bool_v_0(left.value > right.value)
            case "le": result = Primitive_Bool_v_0(left.value <= right.value)
            case "ge": result = Primitive_Bool_v_0(left.value >= right.value)
        append(result,left)
        append(result,right)
        return result
    
    def unary(self,op):
        match op:
            case "neg": result = Primitive_Number_v_0(-self.value)
            case "pos": result = Primitive_Number_v_0(self.value)
        append(result,self)
        return result
