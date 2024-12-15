import time

def fib(n):
    if n<=2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def main(num_iteration):
    execution_times = []
    for i in range(num_iteration):
        s = time.perf_counter()
        fib(20)
        e = time.perf_counter()
        execution_times.append(e - s)
    return execution_times
