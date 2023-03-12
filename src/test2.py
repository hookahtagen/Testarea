"""
    Backup file for the RSA encryption tool

"""
import getpass as gp
import random
import math
import time

import openai
from core_functions.clear_screen import clear_screen
from typing import Optional
from primeGenerator import PrimeGenerator


#
# ***** Openai class *****
#

class ChatGpt:

    def __init__(self, name="ChatGpt", **kwargs):
        self.name = name
        openai.api_key = "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"  # This is not a valid api key. so don't try to use it 
        self.result = ""
        self.kwargs = kwargs

    def input_checker(self, key: str, value: str):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Knowledge cutoff: 2023-03-04 ( YYYY-MM-DD ) Current date: 2023-03-04 ( YYYY-MM-DD )"},
                {"role": "user",
                 "content": "In the following I'll present you a key and a user input. Your task is to check whether the user input is a valid input or not. If the input is valid corresponding to the key, respond only with TRUE. If the input is in some way incorrect try to correct it. By that I mean you should correct wrong characters, e.g. \"\\\" to \"/\" in file paths, grammar and spelling mistakes (in English language) and so on and respond with the updated result. If you have updated the input, respond with the update inpute leaded by \"UPDATED: \". If the input is not valid at all, respond with FALSE. DO NOT PRINT ANY EXPLANATIONS!"},
                {"role": "user", "content": "key: number, value: \"2e-23\""},
                {"role": "assistant", "content": "TRUE"},
                {"role": "user", "content": f"key: {key}, value: {value}"},
            ]
        )

        result = response["choices"][0]["message"]["content"]
        if "UPDATED:" in result:
            result = result.replace("UPDATED: ", "").replace("[", "").replace("]", "").replace("'", "")

        self.result = result


#
# ***** RSA class *****
#


class RSA:

    def __init__(self, pb_key=None, pv_key=None, num_bits=Optional[int], max_tries=Optional[int]):
        self.num_bits = num_bits or 1024
        self.max_tries = max_tries or 1000 * num_bits

        self.primegenerator = PrimeGenerator(self.num_bits, self.max_tries)
        self.primegenerator.start()
        self._prime_cache = {}
        # Check if both keys are None
        if pb_key is None and pv_key is None:
            self._prime_cache = {}
            self._gcd_cache = {}

            self.primegenerator.prime_event.wait()
            self.primegenerator.prime_event.clear()
            self.p = self.primegenerator.prime

            self.primegenerator.prime_event.wait()
            self.primegenerator.prime_event.clear()
            self.q = self.primegenerator.prime

            self.n = pow(self.p, self.q)
            self.phi = (self.p - 1) * (self.q - 1)

            self.e = self.generate_e()
            self.d = self.generate_d()

            self.public_key = (self.e, self.n)
            self.private_key = (self.d, self.n)
        else:
            self.public_key = pb_key
            self.private_key = pv_key

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


def check_input_deprecated(key: str, value: str) -> bool:
    """
    DO NOT USE THIS FUNCTION

    This function will check the user's input
    :param: None
    :return: True if the user's input is valid, False if not
    """
    davinci = ChatGpt()

    davinci.input_checker(key, value)
    if davinci.result == "TRUE":
        val = True
    elif davinci.result == "FALSE":
        val = False
    else:
        print("Error with the input. Possible meant to be: " + davinci.result)
        val = False

    del davinci
    return val


def menu() -> int:
    """
    This function will display the menu and return the user's choice
    :param: None
    :return: The user's choice
    """
    clear_screen()
    menu_str = """
    Welcome to the RSA encryption program!
    \n
    Functions:
    \t1. Generate a new key pair
    \t2. Encrypt a message
    \t3. Decrypt a message
    \t4. Exit
    """
    print(menu_str)
    choice = input("Please enter your choice: ")

    if not choice.isdigit():
        print("Please enter a number!")
        time.sleep(2)
        clear_screen()
        return -1

    choice = int(choice)
    if choice < 1 or choice > 4:
        return -1
    return choice


def genereate_key_pair() -> bool:
    val = False

    rsa = RSA()


    return val


def main():
    val = False
    selected_option = menu()
    if selected_option == -1:
        print("Invalid input!")
        print("Returning to the menu...")
        time.sleep(2)
        main()
    if selected_option == 4:
        print("Exiting...")
        time.sleep(2)
        val = True

    if selected_option == 1:
        val = genereate_key_pair()

    return val


if __name__ == "__main__":
    ret = main()
    exit(0 if ret else 1)
