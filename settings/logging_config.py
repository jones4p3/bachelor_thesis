import logging

def setup_logging(params):
    formatter = logging.Formatter(
    # "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
    "%(levelname)s | %(name)s | %(message)s"
)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    # Set the logging level based on the parameter settings
    root_logger.setLevel(level=params.logging_level)
    root_logger.addHandler(console_handler)