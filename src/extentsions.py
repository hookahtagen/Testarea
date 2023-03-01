import logging


class NoiseLog:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

        file_handler = logging.FileHandler('../log/noise_detail.log')
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

    def formatted_log(self, message: str):
        indentation = ' ' * 4
        formatted_message = '{}{}'.format(indentation, message)
        self.logger.info(formatted_message)
