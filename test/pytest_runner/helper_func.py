# クラス名の検査
def isSameClass(name, class_name):
    return str(type(name)) == f"<class '{class_name}'>"

def isSameValue(created_value, test_value):
    return created_value == test_value

def isSameArray(created_array, test_array):
    # 要素数の確認
    if(len(created_array) != len(test_array)):
        return False
    
    # 各要素の一致を確認
    for i in range(len(created_array)):
        if not isSameValue(created_array[i], test_array[i]):
            return False
    
    return True

def hasExpectedVT(value, vt):
    # vt属性を持っているかの確認
    if not hasattr(value, "vt"):
        return False
    
    # vtの中身の一致確認
    if not (value.vt == vt):
        return False
    
    return True

def hasVTAttribute(value):
    if not hasattr(value, "vt"):
        return False
    
    return True
