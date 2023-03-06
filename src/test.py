"""
    This program is going to contain the RSA encryption algorithm.
    It will be used to encrypt and decrypt messages and binary data.

"""

import os
import random
import math
import time
from core_functions import clear_screen as clear_screen
import cython


#
# ***** Cython functions *****
#

# Cython function for calculating the factorial of a number n
# noinspection PyUnresolvedReferences
def primes(nb_primes: cython.float):
    """
    Calculate the
    :param nb_primes:
    :return:
    """
    i: cython.int
    p: cython.int[1000]

    if nb_primes > 1000:
        nb_primes = 1000

    if not cython.compiled:  # Only if regular Python is running
        p = [0] * 1000       # Make p work almost like a C array

    len_p: cython.int = 0  # The current number of elements in p.
    # noinspection PyShadowingNames
    n: cython.int = 2
    while len_p < nb_primes:
        # Is n prime?
        # noinspection PyUnboundLocalVariable
        for i in p[:len_p]:
            if n % i == 0:
                break

        # If no break occurred in the loop, we have a prime.
        else:
            p[len_p] = n
            len_p += 1
        n += 1

    # Let's copy the result into a Python list:
    result_as_list = [prime_number for prime_number in p[:len_p]]
    return result_as_list


class RSA:

    def __init__(self):
        self.p = self.generate_large_prime()
        self.q = self.generate_large_prime()
        self.n = pow(self.p, self.q)
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self.generate_e()
        self.d = self.generate_d()
        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)

    def generate_large_prime(self):
        while True:
            num = random.randint(2 ** 64, 2 ** 128)
            if self.is_prime(num):
                return num

    @staticmethod
    def is_prime(num):
        if num % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(num)) + 1, 2):
            if num % i == 0:
                return False
        return True

    def generate_e(self):
        while True:
            e = random.randint(1, self.phi)
            if math.gcd(e, self.phi) == 1:
                return e

    def generate_d(self):
        for d in range(1, self.phi):
            if (d * self.e) % self.phi == 1:
                return d

    def encrypt(self, data):
        return pow(data, self.e, self.n)

    def decrypt(self, data):
        return pow(data, self.d, self.n)

    def encrypt_message(self, msg):
        ret_message = ""
        for char in msg:
            ret_message += chr(self.encrypt(ord(char)))
        return ret_message

    def decrypt_message(self, msg):
        ret_message = ""
        for char in msg:
            ret_message += chr(self.decrypt(ord(char)))
        return ret_message


def menu() -> str:
    """
    This function will print the menu and return the user's option
    :param: None
    :return: option (str) - the selected option
    """
    menu_string_lst = [
        "Welcome to the RSA Encryption Tool",
        "Thank you for using my software :)",
        "Main Menu",
        '',
        "1. Generate RSA Keys",
        "2. Encrypt Message",
        "3. Decrypt Message",
        "4. Exit",
        'Please select an option: '
    ]

    print(menu_string_lst[0] + "\n" + menu_string_lst[1])
    time.sleep(3)
    # print the menu, leave out the first 2 lines and the last line
    for line in menu_string_lst[2:-1]:
        print(line)

    option = input(menu_string_lst[-1])

    return option


def sub_menu(option: int) -> int:
    """
    This function will print the sub menu and return the user's choice
    :param: option (int) - the main menu option
    :return: sub_option (int) - the selected option
    """
    sub_option: int = 0
    if option == 1:
        option_1_str_lst = [
            "Do you want to generate a new key pair while encrypting a message,",
            "or do you want to use an existing key pair?",
            "1. Generate new key pair",
            "2. Use existing key pair",
            "3. Return to main menu",
            "Please select an option: "
        ]
        for line in option_1_str_lst[:-1]:
            print(line)

        sub_option = int(input(option_1_str_lst[-1]))
    elif option == 2:
        pass

    return sub_option


def rsa_handler():
    rsa = RSA()
    message = "Hello World!"
    encrypted_message = rsa.encrypt_message(message)
    decrypted_message = rsa.decrypt_message(encrypted_message)
    print(f"Message: {message}")
    print(f"Encrypted Message: {encrypted_message}")
    print(f"Decrypted Message: {decrypted_message}")


def option_1():
    sub_opt = sub_menu(1)


def main():
    option = menu()

    if option == "1":
        pass
    elif option == "2":
        pass
    elif option == "3":
        pass
    elif option == "4":
        pass
    else:
        print("Invalid option selected")
        print("Program will return to the main menu in 3 seconds")
        time.sleep(3)
        clear_screen()
        main()


if __name__ == "__main__":
    main()
