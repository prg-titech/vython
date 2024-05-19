def hasher1(s):
    if(s=="document"):
        return 8429038
    else:
        return -1

def hasher2(s):
    if(s=="document"):
        return 5405432
    else:
        return -1

class Encryption!1:
    def __init__(self):
        pass
    def hash(self,s):
        return hasher1(s)
        
class Encryption!2:
    def __init__(self):
        pass
    def hash(self, s):
        return hasher2(s)
        # return hasher2(s).incompatible(Encryption, 2)

#--------------------------------------------
#-----------------  main  -------------------
#--------------------------------------------
file_name = "document"

# file名を暗号化して保存
e_v1 = Encryption!1()
encrypted_file_name = e_v1.hash(file_name)

# ~~~~~~~~~~~~~~~

# file名の検索 -> ハッシュ値を用いた比較検査によって検索
target_file_name = "document"
e_v2 = Encryption!2()
encrypted_target_file_name = e_v2.hash(target_file_name)

# if(encrypted_file_name == encrypted_target_file_name):
#     result = True
# else:
#     result = False

result = (encrypted_file_name == encrypted_target_file_name)

# 結果を返す
result


