from PIL import Image


class ImageProcessor:

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

    def encode_image(self, image_file, message):
        # Open the image and convert to RGB format
        img = Image.open(image_file).convert('RGB')

        # Get the size of the image
        width, height = img.size

        # Check if the message is too long to fit in the image
        max_chars = (width * height * 3) // 8 - 4
        if len(message) > max_chars:
            raise ValueError('Message too long to encode in the image')

        # Convert the message to binary format
        message += '\0' * (4 - len(message) % 4)
        binary_message = ''.join(format(ord(c), '08b') for c in message)

        # Add the length of the message to the beginning of the binary data
        binary_length = format(len(message), '032b')
        binary_data = binary_length + binary_message

        # Encode the binary data into the image
        pixels = img.load()
        index = 0
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                if index < len(binary_data):
                    pixels[x, y] = (r & 254 | int(binary_data[index]), g & 254 | int(binary_data[index + 1]),
                                    b & 252 | int(binary_data[index + 2]))
                    index += 3
                else:
                    break

        # Save the image with the message encoded
        output_file = image_file[:-4] + '_encoded.png'
        img.save(output_file)
        return output_file


