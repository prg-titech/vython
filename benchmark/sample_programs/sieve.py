import time

def sieve(flags, size):
    prime_count = 0

    for i in range(2, size + 1):
        if flags[i - 1]:
            prime_count = prime_count + 1
            k = 2 * i
            while k <= size:
                flags[k - 1] = False
                k = k + i

    return prime_count

def main(num_iteration):
    flags = []
    size = 5000
    for flag in range(size):
        flags.append(True)
    execution_times = []
    for iteration in range(num_iteration):
        s = time.perf_counter()
        sieve(flags, size)
        e = time.perf_counter()
        execution_times.append(e - s)
    return execution_times