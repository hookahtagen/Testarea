import logging
import json


class NoiseLogger:
    def __init__(self, level=logging.DEBUG):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.file_handler = logging.FileHandler('../log/noise.log')
        self.file_handler.setLevel(level)
        self.file_handler.setFormatter(self.formatter)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(level)
        self.console_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

    def log_dict(self, file: str, data: dict):
        file_hash = hash(file)
        message = f"Used file: {file}" + "\n" + f"File Hash: {file_hash}" + "\n" + json.dumps(data, indent=4)
        self.logger.info(f"\n{message}")

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
