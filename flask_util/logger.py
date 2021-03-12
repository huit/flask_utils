import logging


#============================================================================================
# Logging
#============================================================================================
def get_common_logger(module_name):
    """
    Function to create and return a new logger for a module
    """
    module_logger = logging.getLogger(module_name)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_format = logging.Formatter(
        '{"log_level": "%(levelname)s", '
        '"app_file_line": "%(name)s:%(lineno)d", '
        '"message": %(message)s}'
        )
    stream_handler.setFormatter(stream_format)
    module_logger.addHandler(stream_handler)
    module_logger.setLevel(logging.INFO)
    return module_logger

