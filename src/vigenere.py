'''
    Author: Hendrik Siemens
    Date: 2023-02-13
    Email: siemenshendrik1@gmail.com
    Version: 2.1
    
    Description:
        This program uses the Vigenere cipher to encrypt and decrypt messages.
        For more security, the Vigenere cipher is used in conjunction with the Polyalphabetic cipher.
        
        For more information about this program, please visit the GitHub repository:
        https://github.com/hookahtagen/PolyVigenere
'''


import argparse
import getpass
import hmac
import logging
import random
from polyAlpha import Alphabet

class Logger:
    
    def __init__( self ):
        self.logger = logging.getLogger( __name__ )
        self.logger.setLevel( logging.DEBUG )

        console_handler = logging.StreamHandler( )
        console_handler.setLevel( logging.INFO )
        self.formatter = logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
        console_handler.setFormatter( self.formatter )
        self.logger.addHandler( console_handler )

        file_handler = logging.FileHandler( '../log/alphabet.log' )
        file_handler.setLevel( logging.DEBUG )
        file_handler.setFormatter( self.formatter )
        self.logger.addHandler( file_handler )

    def info( self, message: str ):
        self.logger.info( message )

    def debug( self, message: str ):
        self.logger.debug( message )

    def warning( self, message: str ):
        self.logger.warning( message )

    def error( self, message: str ):
        self.logger.error( message )

    def critical( self, message: str ):
        self.logger.critical( message )
        
class Machine:
    def __init__( self ) -> None:
        self.initialized = "Machine Initialized"
        return None
        
    def process_message( self, mode: str, key: str, message: str, file_enc: bool, file_name: str ) -> tuple[str, str]:
        self.mode = mode
        self.key = key
        self.message = message
        self.alphabets: dict[ str, str ] = { }
        self.file_enc = file_enc
        
        self.alpha = Alphabet( key )
        self.alphabets = self.alpha.polyalphabet
        
        if self.mode == 'e':
            self.processed_message = self.poly_vigenere_encrypt( self.message, self.key, self.alphabets )
            _, self.mic = self.CIV( self.processed_message, self.key )
        elif self.mode == 'd':
            self.processed_message = self.poly_vigenere_decrypt( self.message, self.key, self.alphabets )
        
        if not self.file_enc:
            if self.mode == 'd':
                return self.processed_message, ''
            return self.processed_message, self.mic
        else:
            with open( file_name.replace('.txt','_enc.txt'), 'w' ) as file:
                file.write( self.processed_message )
            
            if self.mode == 'd':
                return "File decrypted successfully"
            else:
                return "File encrypted successfully"
        
    def poly_vigenere_encrypt(self, plaintext: str, key: str, alphabets: dict[str, str] ) -> str:
        '''
        Description:
            This function takes a plaintext string and a key string and encrypts the plaintext using the key.
            Every character in the plaintext is encrypted using the character in the key that corresponds to it.

        Args:
            plaintext (str): _description_
            key (str): _description_
            alphabets (dict[str, str]): _description_

        Returns:
            str: _description_
        '''    
        
        ciphertext = ""
        key_index = 0
        for char in plaintext:
            if char.upper() in alphabets[key[key_index % len(key)]]:
                key_char = key[key_index % len(key)]
                char_index = alphabets[key_char].find(char.upper())
                ciphertext += alphabets[key_char][(char_index + 1) % len(alphabets[key_char])]
            else:
                ciphertext += char
            key_index += 1
        return ciphertext

    def poly_vigenere_decrypt(self, ciphertext: str, key: str, alphabets: dict[str, str]) -> str:
        '''
        Description:
            This function takes a ciphertext string and a key string and decrypts the ciphertext using the key.
            
        Args:
            ciphertext (str): _description_
            key (str): _description_
            alphabets (dict[str, str]): _description_

        Returns:
            str: _description_
        '''    
        
        plaintext = ""
        key_index = 0
        for char in ciphertext:
            char_index = alphabets[key[key_index % len(key)]].find(char)
            if char_index != -1:
                plaintext += alphabets[key[key_index % len(key)]][alphabets[key[key_index % len(key)]].find(char) - 1]
            else:
                plaintext += char
            key_index += 1
        return plaintext
    
    def CIV(self, message: str, key: str) -> tuple[str, str]:
        """
            Description:
                Encrypt the message and compute a Message Integrity Code (MIC) to ensure the authenticity of the encrypted message.
            Parameters:
                message (str): The message to be encrypted.
                key (str): The key used to encrypt the message.
            Returns:
                encrypted_message (str): The encrypted message.
                mic (str): The Message Integrity Code (MIC) of the encrypted message.
        """

        b_key = key.encode()
        encrypted_message = message.encode()
        
        mic = hmac.new(b_key, encrypted_message, digestmod='sha256')
        mic = mic.hexdigest()

        return encrypted_message, mic

    def verify_CIV(self, encrypted_message, mic, key) -> bool:
        """
            Description:
                Verify the authenticity of the encrypted message using the Message Integrity Code (MIC).
            Parameters:
                encrypted_message (str): The encrypted message.
                mic (str): The Message Integrity Code (MIC) of the encrypted message.
                key (str): The key used to encrypt the message.
            Returns:
                True if the MIC is valid, False otherwise.
        """
        b_key = key.encode()

        computed_mic = hmac.new(b_key, encrypted_message, digestmod='sha256')
        computed_mic = computed_mic.hexdigest()
    
        if mic == computed_mic:
            return True
        else:
            return False

def format_key( key: str ) -> tuple[ str, str ]:
    '''
        Description:
            This function formats the key to be used in the polyalphabetic substitution cipher.
            If the key is less than 32 characters, it is expanded to 32 characters using the characters in the key.
            Then the long key is then randomly shuffled.
        Parameters:
            key (str): The key to be formatted.
        Returns:
            key (str): The entered key.
            long_key (str): The expanded key, if the key is less than 32 characters, None otherwise.
    '''
    long_key = None
    if len( key ) < 32:
        long_key = key
        while len( long_key ) < 32:
            long_key += key
        long_key = ''.join( random.sample( long_key, len( long_key ) ) )
    return key, long_key

def log_output( log: Logger, output_lst: list[ str ] ) -> None:
    '''
        Description:
            This function logs the output of the program.
        Parameters:
            log (Logger): The logger object.
            output_lst (list[ str ]): The list of strings to be logged.
        Returns:
            None
    '''
    for output in output_lst:
        log.info( output )
    

def main( log: Logger ) -> None:
    '''
        Description:
            This function is the main function of the program.
            It is responsible for the user interface and the interaction with the user.
        Parameters:
            log (Logger): The logger object.
        Returns:
            None
    '''
    ret = 1
    machine = Machine( )
    main_str_dict: dict[ str, str ] = {
        'Welcome_message': 'Welcome to the PolyVigenere Machine',
        'settings_file': 'You have either the option to use the settings file or enter the settings manually',
        'use_settings_file': 'Do you want to use the settings file? (y/n): ',
        'file_enc': 'Do you want to encrypt or decrypt a file? (y/n): ',
        'mode': 'Do you want to encrypt or decrypt a message? (e/d): ',
        'key': 'Enter the key: ',
        'message': 'Enter the message: ',
        'file_name': 'Enter the file name: ',
    }
    log.info( machine.initialized )

    print( main_str_dict[ 'Welcome_message' ] )
    print( main_str_dict[ 'settings_file' ] )
    settings_file: bool = True if input( main_str_dict['use_settings_file'] ) == 'y' else False
    
    file_enc: bool = True if input( main_str_dict['file_enc'] ) == 'y' else False
    mode = input( main_str_dict['mode'] )
    if settings_file:
        in_settings: dict[ str, str ] = { }
        with open( '../data/settings.cfg', 'r' ) as in_file:
            for line in in_file:
                line = line.strip()
                a_key, value = line.split( '=' )
                in_settings[ a_key ] = value
        key = in_settings[ 'key' ].upper( )
        
        in_key, key = format_key( key )
            
    elif not settings_file:
        key = getpass.getpass( main_str_dict['key'] ).upper( )
        in_key, key = format_key( key )
        
    if not file_enc:
        message = input( main_str_dict['message'] )
        p_message, mic = machine.process_message( mode, key, message, file_enc, None )
        
        output_lst = [ f'Processed Message: {p_message}', f'Message Integrity Code: {mic}', f'Entered Key: {in_key}', f'Key used for encryption: {key}' ]
        log_output( log, output_lst )
        
        ret = 0
    elif file_enc:
        file_name = input( main_str_dict['file_name'] )
        with open( file_name, 'r' ) as file:
            message = file.read( )
        p_message, mic = machine.process_message( mode, key, message, file_enc, file_name )
        
        output_lst = [ f'Processed Message: {p_message}', f'Message Integrity Code: {mic}', f'Entered Key: {in_key}', f'Key used for encryption: {key}' ]
        log_output( log, output_lst )

        ret = 1 

    return ret

def line_args():
    help_text_dict = {
        'verify': 'Verify the authenticity of the encrypted message using the Message Integrity Code (MIC).'
    }
    parser = argparse.ArgumentParser( )
    parser.add_argument( '-v', '--verify', help=help_text_dict['verify'], action='store_true' )
    args = parser.parse_args( )
    
    return args.verify
    

if __name__ == '__main__':
    verify = line_args( )
    log = Logger( )    
    
    if not verify:
        ret = main( log )    
        exit( ret )
        
    elif verify:
        
        key = getpass.getpass( 'Enter the key: ' ).upper( )
        message = input( 'Enter the message: ' )
        mic = input( 'Enter the Message Integrity Code (MIC): ' )
        
        machine = Machine( )
        valid = machine.verify_CIV( message.encode( ), mic, key )
        
        log.info( f'Is the message authentic? {valid}' )