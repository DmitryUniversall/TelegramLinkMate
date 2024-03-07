import os
import sys
import logging
from typing import Self, Optional
from src.core.utils.syntax import default
from .formatters import ConsoleLogFormatter, FileLogFormatter


class LoggerBuilder:
    """
    A builder class for creating and configuring loggers.

    Attributes:
    - `DEFAULT_CONSOLE_LOG_FORMATTER`: `logging.Formatter`
        The default console log formatter (`ConsoleLogFormatter`).

    - `DEFAULT_FILE_LOG_FORMATTER`: `logging.Formatter`
        The default file log formatter (`FileLogFormatter`).

    Methods:
    - `__init__(self, name: str, level: int = logging.INFO) -> None`
        Initializes the LoggerBuilder instance.

    - `enable_console(self, level: int = logging.INFO, formatter: Optional[logging.Formatter] = None) -> Self`
        Adds a `logging.StreamHandler` with `sys.stdout` stream to the logger for console logging.

    - `add_file(self, path: str, level: int = logging.INFO, formatter: Optional[logging.Formatter] = None, encoding: Optional[str] = None) -> Self`
        Adds a `logging.FileHandler` to the logger for logging to a file.

    - `get(self) -> logging.Logger`
        Returns the created logger (`logging.Logger`) object.
    """

    DEFAULT_CONSOLE_LOG_FORMATTER: logging.Formatter = ConsoleLogFormatter()
    DEFAULT_FILE_LOG_FORMATTER: logging.Formatter = FileLogFormatter()

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        """
        Creates the logger and initializes LoggerBuilder

        :param name: `str`
            Logger name

        :param level: `Optional[int]`
            (Optional) Log level for logger.
            By default, `logging.INFO`
        """

        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)

    def enable_console(self, level: int = logging.INFO, formatter: Optional[logging.Formatter] = None) -> Self:
        """
        Adds `logging.StreamHandler` with `sys.stdout` stream to logger, for logs to be displayed in the console

        :param level: `Optional[int]`
            (Optional) Log level for StreamHandler.
            By default, `logging.INFO`

        :param formatter: `Optional[logging.Formatter]`
            (Optional) Formatter for StreamHandler

        :return: `Self`
            LoggerBuilder object (self)
        """

        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setFormatter(default(formatter, self.DEFAULT_CONSOLE_LOG_FORMATTER))
        console_handler.setLevel(level)

        self._logger.addHandler(console_handler)
        return self

    def add_file(self,
                 path: str,
                 level: int = logging.INFO,
                 formatter: Optional[logging.Formatter] = None,
                 encoding: Optional[str] = None
                 ) -> Self:
        """
        Adds `logging.FileHandler` to logger, for logs to be saved to the specified file

        :param path: `str`
            Path to log file

        :param level: `Optional[int]`
            (Optional) Log level for FileHandler

        :param formatter: `Optional[logging.Formatter]`
            (Optional) Formatter for FileHandler

        :param encoding: `Optional[str]`
            (Optional) Encoding of the log file

        :return: `Self`
            LoggerBuilder object (self)
        """

        os.makedirs(os.path.dirname(path), exist_ok=True)

        info_file_handler = logging.FileHandler(
            filename=path,
            encoding=default(encoding, "utf-8")
        )
        info_file_handler.setFormatter(default(formatter, self.DEFAULT_CONSOLE_LOG_FORMATTER))
        info_file_handler.setLevel(level)

        self._logger.addHandler(info_file_handler)
        return self

    def get(self) -> logging.Logger:
        """
        Returns created logger (`logging.Logger`) object

        :return: `logging.Logger`
            Created logger (`logging.Logger`) object
        """

        return self._logger
