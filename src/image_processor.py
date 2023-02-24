from PIL import Image


class ImageProcessor:
    """ImageProcessor

        Description:
            This class is used to encode a process an image.
        Attributes:
            name (str): The name of the ImageProcessor object.
        Methods:
            encode_image(image_file, message) -> str
    """

    def __int__(self, name="ImageProcessor"):
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

    @staticmethod
    def p_continue(self):
        """p_continue

            Description:
                This method is used to pause the program and wait for user input.
            Args:
            Returns:
                None
        """

        continue_message = "Press any key to continue..."
        _ = input(continue_message)

    @staticmethod
    def encode_image(self, image_path, message):
        # Open the image and convert it to RGB format
        image = Image.open(image_path).convert('RGB')

        # Get the width and height of the image
        width, height = image.size

        # Convert the message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in message)

        # Check if the length of the binary message is less than or equal to the number of pixels in the image
        max_message_length = width * height * 3 // 8
        if len(binary_message) > max_message_length:
            raise ValueError('Message too long to embed in the image.')

        # Embed the message in the image using LSB steganography
        binary_message += '0' * (max_message_length - len(binary_message))
        pixels = list(image.getdata())
        new_pixels = []
        for i in range(0, max_message_length, 3):
            pixel = pixels[i // 3]
            new_pixel = (
                pixel[0] & ~1 | int(binary_message[i]),
                pixel[1] & ~1 | int(binary_message[i + 1]),
                pixel[2] & ~1 | int(binary_message[i + 2])
            )
            new_pixels.append(new_pixel)

        print(f'Length of pixel data: {len(pixels)}')
        print(f'Length of new pixel data: {len(new_pixels)}')

        # Create a new image from the modified pixels and save it
        # noinspection PyTypeChecker
        new_image = Image.new(image.mode, image.size)
        # noinspection PyTypeChecker
        new_image.putdata(new_pixels)
        print(f'Encoded image saved to {image_path.replace(".", "_encoded.")}.')
        new_image.save(image_path.replace('.', '_encoded.'))

        self.p_continue(self)

    @staticmethod
    def extract_text_from_image(self, image_path):
        # Open the image and convert it to RGB format
        image = Image.open(image_path).convert('RGB')

        # Get the width and height of the image
        width, height = image.size

        # Extract the message from the image using LSB steganography
        pixels = list(image.getdata())
        binary_message = ''
        for pixel in pixels:
            binary_message += str(pixel[0] & 1)
            binary_message += str(pixel[1] & 1)
            binary_message += str(pixel[2] & 1)

        # Convert the binary message back to ASCII text
        message = ''
        for i in range(0, len(binary_message), 8):
            message += chr(int(binary_message[i:i + 8], 2))

        # Return the extracted message
        return message.strip('\0')
