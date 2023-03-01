import cv2
import numpy as np


def encode_message(image, msg, output_path):
    # Convert message to binary
    message_bits = ''.join(format(ord(c), '08b') for c in msg)

    # Generate random noise
    noise = np.random.normal(scale=10, size=image.shape)

    # Flatten noise and message arrays
    flat_noise = noise.ravel()
    flat_message = np.array([int(bit) for bit in message_bits]).ravel()

    # Compute modified noise array
    encoded_noise = flat_noise.copy()
    encoded_noise[:len(flat_message)] += flat_message

    # Reshape encoded noise into image shape
    encoded_noise = encoded_noise.reshape(image.shape)
    encoded_imag = image + encoded_noise

    # Save encoded image as PNG file
    cv2.imwrite(output_path, encoded_imag)

    return encoded_imag


def decode_message(original_img, encoded_img):
    # Extract noise from encoded image
    noise = encoded_img - original_img

    # Flatten noise array
    flat_noise = noise.ravel()

    # Find indices of message bits in noise array
    message_indices = np.where(abs(flat_noise[:800]) > 5)[0]

    # Extract message bits from noise array
    message_bits = (flat_noise[message_indices] > 0).astype(int)

    # Convert message bits to characters
    msg = ''.join(chr(int(''.join([str(bit) for bit in message_bits[i:i + 8]]), 2)) for i in range(0, len(message_bits), 8))

    return msg


original_image = cv2.imread('../data/test.png')
encoded_image = cv2.imread('../data/encoded.png')
message = decode_message(original_image, encoded_image)

print(message)
