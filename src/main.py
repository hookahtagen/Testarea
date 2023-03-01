"""
    Author:         Hendrik Siemens
    Date:           2023-02-25
    Version:        1.0.0

    Description:
                    This is the main file for the LSB Steganography tool.
                    It is used to encode and decode messages in images.
                    It uses the ImageProcessor class to do the actual encoding and decoding.

    Usage:
                    python3 main.py

    License:
                    MIT License

    Changelog:
                    2023-02-25  Hendrik Siemens 1.0.0   Initial version

"""


import time
from image_processor import ImageProcessor
from types import SimpleNamespace
from vigenere import Machine

#
# ***** Defines *****
#

env: SimpleNamespace

#
# *******************
#


# noinspection PyArgumentList
def encode_message(img: ImageProcessor):
    global env
    str_lst = [
        f'Encoding message: {env.message}',
        'Done!'
    ]
    algorithms = [
        img.encode_into_lsb,
        img.encode_statistical_steganography
    ]

    if env.algorithm in ['least_significant_bit', 'lsb']:
        algorithms[0]()
    elif env.algorithm in ['statistical', 'stat']:
        algorithms[1]()

    print(str_lst[0])
    time.sleep(1)
    print(str_lst[1])


# noinspection PyArgumentList
def extract_message(img: ImageProcessor):
    global env
    str_lst = [
        f'Extracting message from: {env.in_file}',
        f'Extracted message: ',
        'Done!'
    ]
    algorithms = [
        img.extract_from_lsb,
        img.extract_statistical_steganography
    ]

    print(str_lst[0])
    time.sleep(1)
    if env.algorithm in ['least_significant_bit', 'lsb']:
        algorithms[0]()
    elif env.algorithm in ['statistical', 'stat']:
        algorithms[1]()

    str_lst[1] += img.out_message

    print(str_lst[1])
    print(str_lst[2])


def exit_program():
    exit_msg = """
    Thank you for using the LSB Steganography tool!
    Goodbye!"""
    print(exit_msg)
    exit(0)


def get_menu():
    menu = """
    Welcome to the LSB Steganography tool!
    Please select an option from the list below:
        1. Encode a message into an image
        2. Extract a message from an image
        3. Exit    
    """
    return menu


# def check_input(in_str: str) -> bool:
#     pass


# noinspection PyUnboundLocalVariable
def get_input(mode: int):
    in_file = input('Enter the path to the image: ')
    algorithm = input('Enter the algorithm to use: ')
    message = input('Enter the message to encode: ') if mode == 1 else None
    ret_message = message.encode() if mode == 1 else None

    return in_file, ret_message, algorithm


def main():
    global env

    print(_ := get_menu())

    option = int(input('Option: '))
    env.in_file, env.message, env.algorithm = get_input(option)
    options = {
        1: encode_message,
        2: extract_message,
        3: exit_program
    }

    # Initialize the ImageProcessor object with the name, path and message in kwargs
    env.img = ImageProcessor(img_path=env.in_file, in_message=env.message)

    options[option](env.img if option != 3 else None)


def setup():
    global env
    env = SimpleNamespace()

    env.machine = Machine()
    env.flag = False


if __name__ == '__main__':
    setup()  # Setup the environment variables
    main()
