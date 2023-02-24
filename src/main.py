from image_processor import ImageProcessor


def encode_message(img: ImageProcessor):
    in_file = "/home/hendrik/Documents/Github/Testarea/data/test.png"
    message = "Hello World! This is just a löööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööööötest."
    out_file = img.encode_image(img, in_file, message)

    print(f'Encoded image saved to {out_file}.')
    print('Done!')


def extract_message(img: ImageProcessor):
    in_file = "/home/hendrik/Documents/Github/Testarea/data/test_encoded.png"

    message = img.extract_text_from_image(img, in_file)
    print(f'Extracted message: {message}')
    print('Done!')


def main():
    img = ImageProcessor()

    option: int = int(input("1. Encode message\n2. Extract message\n"))

    options = {
        1: encode_message,
        2: extract_message
    }

    options[option](img)


if __name__ == '__main__':
    main()
