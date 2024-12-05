import time

def fib(n):
    if n<=2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

s = time.perf_counter()
fib(20)
e = time.perf_counter()
print(e - s)
