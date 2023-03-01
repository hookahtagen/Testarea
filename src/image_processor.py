import numpy as np
from PIL import Image


# noinspection PyTypeChecker,DuplicatedCode
class ImageProcessor:
    """ImageProcessor
        Description:
            This class is used to provide methods for doing various image processing tasks.
            For details on the methods, please see the documentation.
        Attributes:
            name (str): The name of the ImageProcessor object.
        Methods:
            encode_image(image_file, message) -> str
    """

    def __init__(self, name="ImageProcessor", **kwargs):
        """Constructor

            Description:
                This is the constructor for the ImageProcessor class.
                It is used to initialize the class/the ImageProcessor object.
            Args:
                None
            Returns:
                None
        """
        self.name = name
        self.encode_extension = "_encoded.png"
        self.continue_message = "Press any key to continue..."
        self.out_message = ""

        self.img_path = kwargs.get("img_path", "")
        self.in_message = kwargs.get("in_message", "")
        print("Message to be encoded: ", self.in_message) if self.in_message else None

    def p_continue(self):
        """p_continue

            Description:
                This method is used to pause the program and wait for user input.
            Args:
            Returns:
                None
        """

        input(self.continue_message)

    @staticmethod
    def calculate_noise(image):
        """calculate_noise

            This function is used to calculate the noise in an image.
            It takes the image as an argument and returns the noise value.

            :param image: The image to calculate the noise for.
            :return std: The noise value.
        """

        std = np.std(image)
        return std

    def encode_into_lsb(self):
        """Text Encoder
            Description:
                This method is used to encode text into an image.
                It uses LSB steganography to encode the message into the image.
            Args:
                self (ImageProcessor): The ImageProcessor object.
            Returns:
                None
        """

        image = Image.open(self.img_path).convert('RGB')

        width, height = image.size
        max_message_length = width * height * 3 // 8

        binary_message = ''.join(format(ord(char), '08b') for char in self.in_message)

        if len(binary_message) > max_message_length:
            raise ValueError('Message too long to embed in the image.')

        binary_index = 0
        pixels = list(image.getdata())
        for i in range(0, len(binary_message), 3):
            pixel = list(pixels[i])
            for j in range(3):
                if binary_index < len(binary_message):
                    pixel[j] = pixel[j] & ~1 | int(binary_message[binary_index])
                    binary_index += 1
                else:
                    break
            pixels[i] = tuple(pixel)

        # Save the encoded image
        image.putdata(pixels)
        image.save(self.img_path)

        self.p_continue()

    def extract_from_lsb(self):
        """Text Extractor
            Description:
                This method is used to extract text from an image.
            Args:
                image_path (str): The path to the image.
            Returns:
                None
                :param self: 
        """
        # Open the image and convert it to RGB format
        image = Image.open(self.img_path).convert('RGB')

        # Get the width and height of the image
        width, height = image.size

        # Extract the message from the image using LSB steganography
        binary_message = ''
        pixels = list(image.getdata())
        for i in range(0, width * height, 3):
            pixel = pixels[i]
            for j in range(3):
                binary_message += str(pixel[j] & 1)
            if len(binary_message) % 8 == 0:
                if chr(int(binary_message[-8:], 2)) == '\x00':
                    break

        self.out_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))
        self.out_message = self.out_message.split('!!!')[0]

    def encode_noise_steno(self):
        """Noise Steganography Encoder
            Description:
                This method is used to encode text into an image.
                It uses noise steganography to encode the message into the image.
            Args:
                self (ImageProcessor): The ImageProcessor object.
            Returns:
                None
        """

        image = Image.open(self.img_path).convert('RGB')
