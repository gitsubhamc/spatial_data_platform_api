import logging
import os

class Logger:
    """
    A custom logger class that provides a simple and consistent way to log messages.
    """

    def __init__(self, name: str, log_file: str = "app.log", log_level: str = "INFO"):
        """
        Initializes the logger.

        Args:
            name (str): The name of the logger. This is often the name of the module.
            log_file (str): The path to the log file. Defaults to "app.log".
            log_level (str): The logging level (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"). Defaults to "INFO".
        """

        self.logger = logging.getLogger(name)
        self._set_log_level(log_level)
        
        # Create formatter with timestamp
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Create file handler
        self._create_file_handler(log_file, formatter)

    def _set_log_level(self, log_level: str):
        """
        Sets the logging level based on the provided string.
        
        Args:
            log_level (str): The logging level as a string.
        """
        log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        
        if log_level.upper() in log_levels:
            self.logger.setLevel(log_levels[log_level.upper()])
        else:
            raise ValueError(f"Invalid log level: {log_level}. Supported levels are: {list(log_levels.keys())}")

    def _create_file_handler(self, log_file: str, formatter: logging.Formatter):
        """
        Creates a file handler for logging to a file.
        
        Args:
            log_file (str): The path to the log file.
            formatter (logging.Formatter): The formatter to use for the file handler.
        """
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):  # Check if directory is not empty string and doesn't exist
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str):
        """Logs a debug message."""
        self.logger.debug(message)

    def info(self, message: str):
        """Logs an info message."""
        self.logger.info(message)

    def warning(self, message: str):
        """Logs a warning message."""
        self.logger.warning(message)

    def error(self, message: str):
        """Logs an error message."""
        self.logger.error(message)

    def critical(self, message: str):
        """Logs a critical message."""
        self.logger.critical(message)

    def exception(self, message: str):
        """
        Logs an exception message.
        
        Args:
            message (str): The message to log.
        """
        self.logger.exception(message)



