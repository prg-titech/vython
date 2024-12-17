import time

def fib_pure(n):
    if n<=2:
        return 1
    else:
        return fib_pure(n-1) + fib_pure(n-2)

def main_pure(num_iteration):
    execution_times = []
    for i in range(num_iteration):
        s = time.perf_counter()
        fib_pure(20)
        e = time.perf_counter()
        execution_times.append(e - s)
    return execution_times
