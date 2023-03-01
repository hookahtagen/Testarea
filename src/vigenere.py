"""
    Author: Hendrik Siemens
    Date: 2023-02-13
    Email: siemenshendrik1@gmail.com
    Version: 2.1

    Description:
        This program uses the Vigenere cipher to encrypt and decrypt messages.
        For more security, the Vigenere cipher is used in conjunction with the Polyalphabetic cipher.

        For more information about this program, please visit the GitHub repository:
        https://github.com/hookahtagen/PolyVigenere
"""

import argparse
import getpass
import hmac
import logging
import random
from polyAlpha import Alphabet


class Logger:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

        file_handler = logging.FileHandler('../log/alphabet.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def info(self, info_message: str):
        self.logger.info(info_message)

    def debug(self, debug_message: str):
        self.logger.debug(debug_message)

    def warning(self, warning_message: str):
        self.logger.warning(warning_message)

    def error(self, error_message: str):
        self.logger.error(error_message)

    def critical(self, critical_message: str):
        self.logger.critical(critical_message)


# noinspection PyAttributeOutsideInit
class Machine:
    def __init__(self):
        self.initialized = "Machine Initialized"

    def process_message(self, mode: str, in_key: str, in_message: str, file_enc: bool, file_name: str) -> tuple[str, str]:
        self.mode = mode
        self.key = in_key
        self.message = in_message
        self.alphabets: dict[str, str] = {}
        self.file_enc = file_enc

        self.alpha = Alphabet(in_key)
        self.alphabets = self.alpha.polyalphabet

        if self.mode == 'e':
            self.processed_message = self.poly_vigenere_encrypt(self.message, self.key, self.alphabets)
            _, self.mic = self.civ(self.processed_message, self.key)
        elif self.mode == 'd':
            self.processed_message = self.poly_vigenere_decrypt(self.message, self.key, self.alphabets)

        if not self.file_enc:
            if self.mode == 'd':
                return self.processed_message, ''
            return self.processed_message, self.mic
        else:
            with open(file_name.replace('.txt', '_enc.txt'), 'w') as file:
                file.write(self.processed_message)

            if self.mode == 'd':
                return "File decrypted successfully", ''
            else:
                return "File encrypted successfully", ''

    @staticmethod
    def poly_vigenere_encrypt(plaintext: str, encrypt_key: str, alphabets: dict[str, str]) -> str:
        """
        Description:
            This function takes a plaintext string and a key string and encrypts the plaintext using the key.
            Every character in the plaintext is encrypted using the character in the key that corresponds to it.

        Args:
            plaintext (str): _description_
            encrypt_key (str): _description_
            alphabets (dict[str, str]): _description_

        Returns:
            str: _description_
        """

        ciphertext = ""
        key_index = 0
        for char in plaintext:
            if char.upper() in alphabets[encrypt_key[key_index % len(encrypt_key)]]:
                key_char = encrypt_key[key_index % len(encrypt_key)]
                char_index = alphabets[key_char].find(char.upper())
                ciphertext += alphabets[key_char][(char_index + 1) % len(alphabets[key_char])]
            else:
                ciphertext += char
            key_index += 1
        return ciphertext

    @staticmethod
    def poly_vigenere_decrypt(ciphertext: str, decrypt_key: str, alphabets: dict[str, str]) -> str:
        """
        Description:
            This function takes a ciphertext string and a key string and decrypts the ciphertext using the key.

        Args:
            ciphertext (str): _description_
            decrypt_key (str): _description_
            alphabets (dict[str, str]): _description_

        Returns:
            str: _description_
        """

        plaintext = ""
        key_index = 0
        for char in ciphertext:
            char_index = alphabets[decrypt_key[key_index % len(decrypt_key)]].find(char)
            if char_index != -1:
                plaintext += alphabets[decrypt_key[key_index % len(decrypt_key)]][alphabets[decrypt_key[key_index % len(decrypt_key)]].find(char) - 1]
            else:
                plaintext += char
            key_index += 1
        return plaintext

    @staticmethod
    def civ(civ_message: str, civ_key: str) -> tuple[bytes, str]:
        """
            Description:
                Encrypt the message and compute a Message Integrity Code (MIC) to ensure the authenticity of the
                encrypted message.
            Parameters:
                civ_message (str): The message to be encrypted.
                civ_key (str): The key used to encrypt the message.
            Returns:
                encrypted_message (str): The encrypted message.
                mic (str): The Message Integrity Code (MIC) of the encrypted message.
        """

        b_key = civ_key.encode()
        encrypted_message = civ_message.encode()

        message_identifier_code = hmac.new(b_key, encrypted_message, digestmod='sha256')
        message_identifier_code = message_identifier_code.hexdigest()

        return encrypted_message, message_identifier_code

    @staticmethod
    def verify_civ(encrypted_message, val_mic, val_key) -> bool:
        """
            Description:
                Verify the authenticity of the encrypted message using the Message Integrity Code (MIC).
            Parameters:
                encrypted_message (str): The encrypted message.
                val_mic (str): The Message Integrity Code (MIC) of the encrypted message.
                val_key (str): The key used to encrypt the message.
            Returns:
                True if the MIC is valid, False otherwise.
        """
        b_key = val_key.encode()

        computed_mic = hmac.new(b_key, encrypted_message, digestmod='sha256')
        computed_mic = computed_mic.hexdigest()

        if val_mic == computed_mic:
            return True
        else:
            return False


def format_key(f_key: str) -> tuple[str, str]:
    """
        Description:
            This function formats the key to be used in the polyalphabetic substitution cipher.
            If the key is less than 32 characters, it is expanded to 32 characters using the characters in the key.
            Then the long key is then randomly shuffled.
        Parameters:
            f_key (str): The key to be formatted.
        Returns:
            key (str): The entered key.
            long_key (str): The expanded key, if the key is less than 32 characters, None otherwise.
    """
    long_key = None
    if len(f_key) < 32:
        long_key = f_key
        while len(long_key) < 32:
            long_key += f_key
        long_key = ''.join(random.sample(long_key, len(long_key)))
    return f_key, long_key


def log_output(logg: Logger, output_lst: list[str]) -> None:
    """
        Description:
            This function logs the output of the program.
        Parameters:
            logg (Logger): The logger object.
            output_lst (list[ str ]): The list of strings to be logged.
        Returns:
            None
    """
    for output in output_lst:
        logg.info(output)


# noinspection PyUnboundLocalVariable
def main(logg: Logger) -> int:
    """
        Description:
            This function is the main function of the program.
            It is responsible for the user interface and the interaction with the user.
        Parameters:
            logg (Logger): The logger object.
        Returns:
            None
    """
    ret_val = 1
    main_machine = Machine()
    main_str_dict: dict[str, str] = {
        'Welcome_message': 'Welcome to the PolyVigenere Machine',
        'settings_file': 'You have either the option to use the settings file or enter the settings manually',
        'use_settings_file': 'Do you want to use the settings file? (y/n): ',
        'file_enc': 'Do you want to encrypt or decrypt a file? (y/n): ',
        'mode': 'Do you want to encrypt or decrypt a message? (e/d): ',
        'key': 'Enter the key: ',
        'message': 'Enter the message: ',
        'file_name': 'Enter the file name: ',
    }
    logg.info(main_machine.initialized)

    print(main_str_dict['Welcome_message'])
    print(main_str_dict['settings_file'])
    settings_file: bool = True if input(main_str_dict['use_settings_file']) == 'y' else False

    file_enc: bool = True if input(main_str_dict['file_enc']) == 'y' else False
    mode = input(main_str_dict['mode'])
    if settings_file:
        in_settings: dict[str, str] = {}
        with open('../data/settings.cfg', 'r') as in_file:
            for line in in_file:
                line = line.strip()
                a_key, value = line.split('=')
                in_settings[a_key] = value
        main_key = in_settings['key'].upper()

        in_key, main_key = format_key(main_key)

    elif not settings_file:
        main_key = getpass.getpass(main_str_dict['key']).upper()
        in_key, main_key = format_key(main_key)

    if not file_enc:
        in_message = input(main_str_dict['message'])
        p_message, result_mic = main_machine.process_message(
            mode,
            main_key,
            in_message,
            file_enc,
            ''
        )

        output_lst = [f'Processed Message: {p_message}', f'Message Integrity Code: {result_mic}', f'Entered Key: {in_key}',
                      f'Key used for encryption: {main_key}']
        log_output(logg, output_lst)

        ret_val = 0
    elif file_enc:
        file_name = input(main_str_dict['file_name'])
        with open(file_name, 'r') as file:
            in_message = file.read()
        p_message, result_mic = main_machine.process_message(mode, main_key, in_message, file_enc, file_name)

        output_lst = [f'Processed Message: {p_message}', f'Message Integrity Code: {result_mic}', f'Entered Key: {in_key}',
                      f'Key used for encryption: {main_key}']
        log_output(logg, output_lst)

        ret_val = 1

    return ret_val


def line_args():
    help_text_dict = {
        'verify': 'Verify the authenticity of the encrypted message using the Message Integrity Code (MIC).'
    }
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verify', help=help_text_dict['verify'], action='store_true')
    args = parser.parse_args()

    return args.verify


if __name__ == '__main__':
    verify = line_args()
    log = Logger()

    if not verify:
        ret = main(log)
        exit(ret)

    elif verify:

        key = getpass.getpass('Enter the key: ').upper()
        message: str = input('Enter the message: ')
        mic = input('Enter the Message Integrity Code (MIC): ')

        machine = Machine()
        valid = machine.verify_civ(message, mic, key)

        log.info(f'Is the message authentic? {valid}')
