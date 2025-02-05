import logging
from dataclasses import dataclass
from src.core.paths import LOG


LOGGING_CONFIG = {
    "crewai": logging.INFO,
    "asyncio": logging.ERROR,
    "urllib3": logging.ERROR,
    "certifi": logging.ERROR,
    "PIL": logging.ERROR,
    "httpcore": logging.ERROR,
    "httpx": logging.ERROR,
    "azure": logging.ERROR,
}


@dataclass
class Logger:

    def __post_init__(self) -> None:
        self.format = '%(levelname)s | %(asctime)s | %(name)s | %(message)s | Function: %(funcName)s | Line: %(lineno)d'
        self.date = '%A | %d/%m/%Y | %X'
        self._configure_logger()
        self.__disregard_this_logs()

    @staticmethod
    def __disregard_this_logs() -> None:
        """Setup logging to suppress unnecessary logs while keeping CrewAI agent outputs."""
        logging.basicConfig(level=logging.WARNING, format="%(message)s")  # Set global log level
        for module, level in LOGGING_CONFIG.items():
            logging.getLogger(module).setLevel(level)

    def _configure_logger(self):
        """Configures the root logger."""
        logging.basicConfig(
            filename=LOG,
            filemode='w',
            format=self.format,
            datefmt=self.date,
            level=logging.DEBUG  # Set to DEBUG to capture all logs
        )

        # Ensure all loggers propagate to the root logger
        logging.getLogger().setLevel(logging.DEBUG)

    @staticmethod
    def log_info(message: str):
        """Logs an info message."""
        logging.info(message)

    @staticmethod
    def log_debug(message: str):
        """Logs a debug message."""
        logging.debug(message)

    @staticmethod
    def log_warning(message: str):
        """Logs a warning message."""
        logging.warning(message)

    @staticmethod
    def log_error(message: str):
        """Logs an error message."""
        logging.error(message)
