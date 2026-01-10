import logging

def attach_app_logger():
    logging_format='%(asctime)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s'
    formatter = logging.Formatter(logging_format)

    file_handler=logging.FileHandler("app.log")
    file_handler.setFormatter(formatter)

    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.WARNING)
    if not app_logger.handlers:
        app_logger.addHandler(file_handler)
    
    app_logger.propagate = False


def logger_setup():
    logging_level=logging.INFO
    logging_format='%(asctime)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s'
    file_handler=logging.FileHandler("app.log")

    logging.basicConfig(
        level=logging_level,
        format=logging_format,
        handlers=[file_handler]
    )

