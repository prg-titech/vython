import re

def re_match(self):
    cn = self.__class__.__name__
    # 正規表現パターン
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

def __vt_init__(self):
    self.vt = []
    cv_pair = re_match(self)
    self.vt.append((cv_pair[0],cv_pair[1],False))
    return

def checkCompatibility(left,right):
    for x in left.vt:
        if(x[2]):
            c = x[0]
            v = x[1]
            for y in right.vt:
                if((y[0]==c) and (y[1]!=v)):
                    raise TypeError(f"Inconsistent Version Usage:\nComparing {c}!{v} and {c}!{y[1]} values")
    for y in right.vt:
        if(y[2]):
            c = y[0]
            v = y[1]
            for x in left.vt:
                if((x[0]==c) and (x[1]!=v)):
                    raise TypeError(f"Inconsistent Version Usage:\nComparing {c}!{x[1]} and {c}!{v} values")
    return

def is_include(left,c,v,b):
    for x in left:
        if (x[0]==c) and (x[1]==v) and (x[2]==b):
            return True
    return False

def insert(value,c,v,b):
    for x in value.vt:
        if((x[0]==c) and (x[1]==v)):
                value.vt.remove(x)
        value.vt.append((c, v, b))
    return

def append(left,right):
    for x in left.vt:
        cx = x[0]
        vx = x[1]
        bx = x[2]
        if is_include(right.vt,cx,vx,bx):
            left.vt.remove(x)      
    # 結合を返す
    for y in right.vt:
        left.vt.append(y)
    return

def incompat(self,value):
    cv_pair = re_match(self)
    insert(value,cv_pair[0],cv_pair[1],True)
    return
