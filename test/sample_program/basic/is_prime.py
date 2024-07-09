def is_prime(n):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    return is_prime_recursive(n, 5)

def is_prime_recursive(n, i):
    if i * i > n:
        return True
    if n % i == 0 or n % (i + 2) == 0:
        return False
    return is_prime_recursive(n, i + 6)

print(is_prime(11))
