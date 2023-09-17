import logging

# logger_manager.py

import logging
from logging.handlers import RotatingFileHandler


# TODO: Add a logger manager class to handle logging
# ! This is not working as expected
# class LoggerManager:
    
#     def __init__(self, logger_name, log_file):
#         self.logger = logging.getLogger(logger_name)
#         self.logger.setLevel(logging.DEBUG)
#         self._setup_file_logging(log_file)
#         # self._setup_console_logging()

#     def _setup_file_logging(self, log_file):
#         log_file_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#         file_handler = RotatingFileHandler(log_file, maxBytes=5000000, backupCount=50)
#         file_handler.setFormatter(logging.Formatter(log_file_format))
#         self.logger.addHandler(file_handler)

#     # def _setup_console_logging(self):
#     #     log_console_format = "%(name)s - %(levelname)s - %(message)s"
#     #     console_handler = logging.StreamHandler()
#     #     console_handler.setFormatter(logging.Formatter(log_console_format))
#     #     self.logger.addHandler(console_handler)

#     def get_logger(self):
#         return self.logger

def setup_logger(logger):
    '''The function `setup_logger` sets up a logger object with a file handler that rotates log files and
    formats log messages.
    
    Parameters
    ----------
    logger
        The `logger` parameter is an instance of the `logging.Logger` class. It is used to configure the
    logger and add a file handler to it.
    
    '''    
    logger.setLevel(logging.INFO)  # Adjust the level as needed

    # Create file handler
    file_handler = logging.handlers.RotatingFileHandler('Logs/debug.log', maxBytes=5000000, backupCount=50)
    formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s - (PID: %(process)d) - Message: %(message)s - %(exc_info)s")
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)
