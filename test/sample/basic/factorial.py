# この書き方はダメ。後で直す
def factorial(n):
    if(n==0):
        return 1
    else:
        return n * factorial(n-1)

# def factorial(n):
#     result = 1
#     if(n==0):
#         result = result * 1
#     else:
#         result = n * factorial(n-1)
#     result

num = 4
factorial(num)
