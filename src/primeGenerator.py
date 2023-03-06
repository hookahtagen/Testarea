import threading
import random

from typing import Optional
from core_functions.clear_screen import clear_screen
from threading import Thread


class PrimeGenerator:
    def __init__(self, num_bits: int = 2048, max_tries: Optional[int] = None):
        self.num_bits = num_bits
        self.max_tries = max_tries or 1000 * num_bits

        self.is_running = False
        self.thread = Thread(target=self.generate_primes)
        self.prime = None
        self.prime_event = threading.Event()

    def generate_primes(self):
        while self.is_running:
            self.generate_prime(self.prime_event)
        print("Prime generation stopped")

    def generate_prime(self, p_event: threading.Event):
        for _ in range(self.max_tries):
            if not self.is_running:
                return
            candidate = random.getrandbits(self.num_bits)
            candidate |= (1 << self.num_bits - 1) | 1  # Ensure that the number is odd and has num_bits bits
            if self.is_prime(candidate):
                self.prime = candidate
                p_event.set()
                return
        raise ValueError("Failed to generate prime numbers within the maximum number of tries.")

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
        while d % 2 == 0:
            d //= 2
            s += 1

        # select the witnesses from the dictionary
        witnesses = witness_dict.get(n, witness_dict[0])

        for a in witnesses:
            if pow(a, d, n) == 1:
                continue
            for r in range(s):
                if pow(a, d * 2 ** r, n) == n - 1:
                    break
            else:
                return False
        return True


if __name__ == '__main__':
    primeGenerator = PrimeGenerator()
    primeGenerator.start()

    current_prime = None
    while True:
        if primeGenerator.prime and primeGenerator.prime != current_prime:
            clear_screen()
            current_prime = primeGenerator.prime
            print(f"New prime found: {primeGenerator.prime}")
