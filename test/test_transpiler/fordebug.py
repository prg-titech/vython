# def fib(n):
#     if(n==0):
#         return 0
#     if(n==1):
#         return 1
#     else:
#         return fib(n-1) + fib(n-2)
def fib(n):
    if((n==0) or (n==1)):
        return 1
    else:
        return fib(n-1) + fib(n-2)

x = fib(10)
print(x)

