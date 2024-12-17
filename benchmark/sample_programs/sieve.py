import time

def sieve_pure(flags, size):
    prime_count = 0

    i = 2
    while i < size + 1:
        if flags[i - 1]:
            prime_count = prime_count + 1
            k = 2 * i
            while k <= size:
                flags[k - 1] = False
                k = k + i
        i = i + 1

    return prime_count

def main_pure(num_iteration):
    flags = []
    size = 5000
    for flag in range(size):
        flags.append(True)
    execution_times = []
    for iteration in range(num_iteration):
        s = time.perf_counter()
        sieve_pure(flags, size)
        e = time.perf_counter()
        execution_times.append(e - s)
    return execution_times
