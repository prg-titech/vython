# この書き方はダメ。後で直す
def factorial(n):
    if(n==0):
        return 1
    else:
        return n * factorial(n-1)

num = 0
factorial(num)

# -> 何もないVObjectが返る(Heap 0)
# 原因はifを脱出するときの返る値を0に統一しているため

# 4/15: fixed(maybe)
