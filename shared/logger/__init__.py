import logging
import logging.config

MAIN_LOGGER_NAME = 'main'


def setup_loggers() -> logging.Logger:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    logger = root.getChild(MAIN_LOGGER_NAME)

    file_handler = logging.FileHandler(
        'runtime.log',
        mode='w',
        encoding='utf-8'
    )

    file_handler.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.INFO)

    console_formatter = logging.Formatter('%(message)s')
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


    stdout_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    return logger


def get_logger(module_name: str) -> logging.Logger:
    logger = logging.getLogger(MAIN_LOGGER_NAME).getChild(module_name)

    return logger
