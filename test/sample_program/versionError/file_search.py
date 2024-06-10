class Hash!1:
    def __init__(self):
        pass
    def hasher(self,s):
        if(s=="document"):
            return 8429038
        else:
            return -1
        
class Hash!2:
    def __init__(self):
        pass
    def hasher(self,s):
        if(s=="document"):
            result = 5405432
            incompat(self, result)
            # result.incompatible(Hash, 2)
            return result
        else:
            return -1


file_name = "document"

# file名を暗号化して保存
h_v1 = Hash!1()
hashed_file_name = h_v1.hasher(file_name)

# file名の検索 -> ハッシュ値を用いた比較検査によって検索
target_file_name = "document"
h_v2 = Hash!2()
hashed_target_file_name = h_v2.hasher(target_file_name)

print(hashed_file_name)
print(hashed_target_file_name)
result = (hashed_file_name == hashed_target_file_name)

# 結果を出力
print(result)
