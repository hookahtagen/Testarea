import threading
import random
import time
import concurrent.futures as cf
# Not used at the moment
import timeit
from typing import Optional

import gmpy2 as gmpy2
from gmpy2 import mpz
from gmpy2 import powmod, f_mod
from core_functions.clear_screen import clear_screen
from threading import Thread

#
# ***** DEFINITIONS *****
#


class GeneratorSettings:

    def __init__(self, name: str):
        self.name = name
        self.max_threads = 4


# noinspection PyShadowingNames
class PrimeGenerator:
    def __init__(self, num_bits: int = 2048, max_tries: Optional[int] = 1000, config: GeneratorSettings = GeneratorSettings("default")):
        self.settings = config
        self.max_threads = self.settings.max_threads or 4
        self.num_bits = num_bits
        self.max_tries = max_tries or 1000 * num_bits

        self.is_running = False
        self.thread = Thread(target=self.generate_primes)
        self.prime = None
        self.canditate_queue = None
        self.validated_primes = None
        self.prime_event = threading.Event()

    def generate_primes(self):
        while self.is_running:
            self.generate_prime(self.prime_event)
        print("Prime generation stopped")

    def generate_prime(self, notify: threading.Event):
        while self.is_running:
            # Generate a list of 4 random candidates for prime numbers
            # Each candidate is a random number with num_bits bits
            # Each candidate will then be tested for primality using the Miller-Rabin test
            # running in parallel, with each thread testing a different candidate
            self.canditate_queue = []
            self.validated_primes = []
            for _ in range(4):
                candidate = random.getrandbits(self.num_bits)
                candidate |= (1 << self.num_bits - 1) | 1
                self.canditate_queue.append(candidate)

            ack = threading.Event()
            self.test_for_primality(ack)

            if ack.is_set():
                ack.clear()
                # Choose a random value from the True values in self.validated_primes and get the index from it
                # Use the index to get the prime number from self.canditate_queue
                validatet_indices = [i for i, x in enumerate(self.validated_primes) if x]
                self.prime = self.canditate_queue[random.choice(validatet_indices)]
                notify.set()

    def test_for_primality(self, event: threading.Event):
        for candidate in self.canditate_queue:
            with cf.ThreadPoolExecutor(max_workers=self.settings.max_threads) as executor:
                result = executor.submit(self.is_prime_preprocess, candidate)
                self.validated_primes.append(result.result())

        # If amount of True in self.validated_primes is greater than 1, set event
        if self.validated_primes.count(True) >= 1:
            event.set()

    def generate_prime_old(self):
        while self.is_running:
            for _ in range(self.max_tries):
                candidate = random.getrandbits(self.num_bits)
                candidate |= (1 << self.num_bits - 1) | 1  # Ensure that the number is odd and has num_bits bits
                if self.is_prime(candidate):
                    self.prime = candidate
                    break

    def start(self):
        self.is_running = True
        self.thread.start()

    def stop(self):
        self.is_running = False
        self.thread.join()

    def update_num_bits(self, num_bits: int):
        self.stop()
        self.num_bits = num_bits
        self.start()

    @staticmethod
    def check_small_primes(number: int):
        # noinspection PyArgumentList
        n_gmpy = mpz(number)
        small_primes = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991
        ]
        for divisor in small_primes:
            if gmpy2.f_mod(n_gmpy, divisor) == 0:
                return False

        return True

    def is_prime_preprocess(self, n: int) -> bool:
        """
        Returns True if n is prime, False otherwise.
        """
        ret = True

        if not self.check_small_primes(n):
            # If n is divisible by any small prime, return False
            ret = False

        if ret:
            # If n is not divisible by any small prime, run the Miller-Rabin test
            ret = self.is_prime(n)

        return ret

    @staticmethod
    def is_prime(n: int) -> bool:
        """
        Returns True if n is prime, False otherwise.
        """
        witness_dict = {
            2047: [2, 3],
            1373653: [2, 3, 5],
            9080191: [31, 73],
            25326001: [2, 3, 5, 7],
            3215031751: [2, 3, 5, 7, 11],
            4759123141: [2, 3, 5, 7, 11, 13],
            0: [2, 7, 61]
        }
        # Handle small values of n
        true_conditions = [
            n > 2,
            n % 2 == 0
        ]
        false_conditions = [
            n == 2,
            n == 3,
        ]
        if not any(true_conditions):
            return False
        if any(false_conditions):
            return True

        # Use deterministic Miller-Rabin test
        d = n - 1
        s = 0
        while f_mod(d, 2) == 0:
            d //= 2
            s += 1

        # select the witnesses from the dictionary
        witnesses = witness_dict.get(n, witness_dict[0])
        n_dict = {
            4759123141: 15,
            3215031751: 14,
            25326001: 12,
            9080191: 9,
            1373653: 8,
            2047: 7,
        }
        iterations = n_dict.get(n, n_dict[0]) if n in n_dict else 6

        for a in witnesses[:iterations]:
            if powmod(a, d, n) == 1:
                continue
            for r in range(s):
                if powmod(a, d * 2 ** r, n) == n - 1:
                    break
            else:
                return False
        return True


# noinspection PyShadowingNames
def exponentiation(base: int, exponent: int):
    res = 1
    for _ in range(exponent):
        res *= base
    return res


def wait_for_event(generator: PrimeGenerator):
    generator.prime_event.wait()
    generator.prime_event.clear()


# noinspection PyShadowingNames
def run_timeit(a, b) -> float:
    rounds = 1000
    return timeit.timeit(lambda: a * b, number=rounds)


if __name__ == '__main__':
    settings = GeneratorSettings("Prime")
    clear_screen()
    flag = 2

    if flag == 1:
        primeGenerator = PrimeGenerator(
            num_bits=128,
            config=settings
        )
        primeGenerator.start()

        bits = [128, 256, 512, 1024, 2048]

        # For each bit calculate 10 primes and track the time calculating each of them and then print the average time and the
        # individual times
        for bit in bits:
            primeGenerator.num_bits = bit
            times = []
            for _ in range(10):
                start_time = time.time()
                primeGenerator.prime_event.wait()
                primeGenerator.prime_event.clear()
                local_time = time.time()
                times.append(local_time - start_time)
            print(f"Average time for {bit} bit primes: {sum(times) / len(times)}")
            print(f"Individual times: {times}")
    elif flag == 2:
        # Generate 2 2048 bit primes
        primeGenerator = PrimeGenerator(
            num_bits=2048,
            max_tries=1000
        )
        primeGenerator.start()

        wait_for_event(primeGenerator)
        p1: int = primeGenerator.prime

        wait_for_event(primeGenerator)
        p2: int = primeGenerator.prime

        primeGenerator.stop()

        # result = p1 * p2
        # print(f"Result: {result}")

        # use timeit to measure the time it takes to calculate the product of the two primes
        total_time = run_timeit(p1, p2)

        rounds = 1000
        print(f"Average time for 1 round out of {rounds} rounds: {total_time / rounds}")
