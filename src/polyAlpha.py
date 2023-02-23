import os
import random as rnd
import string
import logging
import pprint


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

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)


class Alphabet:
    alphabets = {
        'A': 'COKWMJXVYTRBQFNIDHASLZPEGU',
        'B': 'UYQXGRTSKOHVJEADNZMIBWCFPL',
        'C': 'ZIQFCJYENVPMROBDUWTGHXSALK',
        'D': 'AWSHKFJVZBUPILGMQODNREYCTX',
        'E': 'FSLPZKEXANUBJDTQIOMRHCVYWG',
        'F': 'RBVQNPOHMLXFATKWCZDYUSEIJG',
        'G': 'ATMXCEKBRIDSHZFPWNLOUJGVQY',
        'H': 'ACJFEMQXURKPIYSGHZWLOTVBDN',
        'I': 'DXZAPHNYFKJBEGILSCOQTRMUVW',
        'J': 'HFYBPKILXUQTNMWGRSVOECJAZD',
        'K': 'OLNKIUJPMEHBSXVARWYTQFCZDG',
        'L': 'JTIDQPXMGLAUOVZCBENFHSYKRW',
        'M': 'ZREXSNITOQLJCWBHVGMKPYFUAD',
        'N': 'YPROKVDLQUINJFGZMCASHTXBEW',
        'O': 'UOFWPNSRYQHTXKICLZMDEABJVG',
        'P': 'HRGWLASVQKUFZXBNDJTCEIMOPY',
        'Q': 'NBZSHGXVLITJCYKOEDMWUQRPFA',
        'R': 'LTDQYFMNCJRHXZGVIEBKUSWAOP',
        'S': 'EIVDOBYGQZCJNUAKMRWHXTSPFL',
        'T': 'PNKTMAXORCGFJULVSIBYQHWZED',
        'U': 'GCRIDEZAMWSQFVYPHOTNULJBKX',
        'V': 'CTBQNHAWLXMGZKUPDYOEIVJSFR',
        'W': 'HKZMNGPTOIRSABLEVUYJQCFWXD',
        'X': 'IWMUFTORKZXCPJLDGBQYSHANVE',
        'Y': 'QZEIHNJODVLGFBAWMXKPUTYRSC',
        'Z': 'YRKHJNZVSAXLQPWIGTEUFBCOMD'
    }

    def __init__(self, key: str) -> None:
        self.key = key
        if self.key != '0':
            self.polyalphabet = self.get_alpha(self.key)

    def get_alpha(self, key: str) -> dict[str, str]:
        alphabets: dict[str, str] = {}

        # For every char in the key append the corresponding dict entry
        # to the variable 'alphabets'

        for char in key:
            alphabets[char] = self.alphabets[char]

        return alphabets

    def generate_alphabet(self, abc_count=4):
        abc = ''
        abc_dict = {}

        def get_key_value(number: int) -> str:
            val_dict = {
                '1': 'A',
                '2': 'B',
                '3': 'C',
                '4': 'D',
                '5': 'E',
                '6': 'F',
                '7': 'G',
                '8': 'H',
                '9': 'I',
                '10': 'J',
                '11': 'K',
                '12': 'L',
                '13': 'M',
                '14': 'N',
                '15': 'O',
                '16': 'P',
                '17': 'Q',
                '18': 'R',
                '19': 'S',
                '20': 'T',
                '21': 'U',
                '22': 'V',
                '23': 'W',
                '24': 'X',
                '25': 'Y',
                '26': 'Z'
            }

            key_name = val_dict[str(number)]

            return key_name

        for i in range(abc_count):
            abc = list(string.ascii_uppercase)
            rnd.shuffle(abc)
            # Optional code for the future:
            # roman_num = getKey_value( i + 1 )
            key_name = get_key_value(i + 1)
            abc_dict[f'{key_name}'] = ''.join(abc)

        return abc_dict

    def save_alpha(self, abc_dict: dict[str, str], log: Logger):
        ret: int = 1

        out_file = '../data/alphabets.txt'

        with open(out_file, 'w') as out:
            for key, value in abc_dict.items():
                out.write(f'\'{key}\' : \'{value}\'\n')
                ret = 0

        log.info(f'Success!')
        log.info(f'Wrote {len(abc_dict)} alphabets to \'{out_file}\'.')
        message = f'Note:\nIn order to use the generated alphabets, please copy\nthe contents of alphabets.txt, ' \
                  f'found in \'/data\' to\nthe variable \'alphabets\' in the file \'polyAlpha.py\'\n'
        print(message)
        return ret


def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def main(custom_logger: Logger) -> None:
    abc = Alphabet('0')
    alpha = {}

    in_text = 'How many alphabets do you want to generate? You can choose up to 26 alphabets. Num alphabets> '
    abc_count = int(input(in_text))
    if abc_count > 26:
        print('You can only generate up to 26 alphabets!')
        print('The limit has been set to 26 alphabets.')

        abc_count = 26
    alpha = abc.generate_alphabet(abc_count)

    print('Below you\'ll find the generated alphabets:\n')
    p_print = pprint.PrettyPrinter(indent=4)
    p_print.pprint(alpha)
    save_alpha = input('\n\nDo you want to save the generated alphabets to the program? (y/n) > ').lower()

    ret = 1
    if save_alpha == 'y':
        ret = abc.save_alpha(alpha, custom_logger)
    elif save_alpha == 'n':
        print('Alphabets not saved!')
        ret = 1
    else:
        print('Invalid input!')
        ret = 1

    exit(ret)



if __name__ == '__main__':
    log = Logger()

    main(log)
