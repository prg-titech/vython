# envに関するbag, interpreterで適切にenvを指定していなかった
# (具体例)interpret_Exprでenvをglobal_envで評価していた。
a = 1
def id():
    a = 2
    return a + 2

id()
# => 3が返っていた

# Exprに包まれていないこれは正しい挙動をする
a = 1
def id():
    a = 2
    return a

id()
# => 2が返る

# 4/15: fixed
