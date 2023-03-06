import random
import time
from sympy import nextprime
from sympy.ntheory import primorial, igcd
from sympy.core.numbers import igcdex
from sympy import mod_inverse
from sympy.ntheory import isprime

_PRIME_CACHE = {}


def generate_prime(number_bits: int = 2048, max_tries: int = 64) -> int:
    # Check if we have already generated a prime with the given parameters
    key = (number_bits, max_tries)
    if key in _PRIME_CACHE:
        return _PRIME_CACHE[key]

    # Start with a random odd number
    p = random.getrandbits(number_bits)
    p |= (1 << number_bits - 1) | 1

    # Keep incrementing by 2 until a prime is found
    while not ECPP(p, max_tries):
        p = nextprime(p + 2)

    # Cache the result and return it
    _PRIME_CACHE[key] = p
    return p


def is_probably_prime(n, k):
    """Test if n is probably prime using k iterations of Miller-Rabin."""
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # Write n-1 as 2^r*d where d is odd
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Test k times
    for _ in range(k):
        a = random.randint(2, n-2)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(r-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False

    return True


def ECPP(p, max_trial=10):
    if isprime(p):
        return True
    N = primorial(100) // primorial(99)
    for trial in range(max_trial):
        a = random.randint(1, p-1)
        if igcd(a, p) != 1:
            return False
        f = pow(a, (p-1) // 2, p)
        if f != 1 and f != p-1:
            return False
        v = (pow(a, p, p*N) - a) % (p * N)
        d = igcd(v, N)
        if d == 1:
            continue
        _, s, t = igcdex(v // d, N // d)
        u = (s * v // d) % (N // d)
        if u % 2 == 0:
            u += N // d
        q = p - u
        if is_probably_prime(q):
            return True
    return False


def s


if __name__ == '__main__':
    rounds = 100
    total_time = 0

    for i in range(rounds):
        start = time.time()
        _ = generate_prime(2048, 64)
        end = time.time()
        total_time += end - start

    print(f"Total time: {total_time}")
    print(f"Average time: {total_time / rounds}")
