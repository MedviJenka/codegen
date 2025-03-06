import logging
from dataclasses import dataclass
from event_recorder.core.paths import LOG

# Define which logs to suppress
LOGGING_CONFIG = {
    "crewai": logging.INFO,
    "asyncio": logging.ERROR,
    "urllib3": logging.ERROR,
    "certifi": logging.ERROR,
    "PIL": logging.ERROR,
    "httpcore": logging.ERROR,
    "httpx": logging.ERROR,
    "azure": logging.ERROR,
    "LiteLLM": logging.ERROR,  # Explicitly suppress LiteLLM logs
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

        # Explicitly disable logs from unwanted modules
        for module, level in LOGGING_CONFIG.items():
            log = logging.getLogger(module)
            log.setLevel(level)
            log.propagate = False  # Prevent propagation to root logger

    def _configure_logger(self):
        """Configures the root logger."""
        handler = logging.FileHandler(LOG, mode='w')
        handler.setLevel(logging.DEBUG)  # Capture DEBUG logs only for root logging
        handler.setFormatter(logging.Formatter(self.format, self.date))

        # Get the root logger and apply the handler
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(handler)

        # Ensure suppressed logs do not propagate
        for module in LOGGING_CONFIG:
            logging.getLogger(module).propagate = False

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
