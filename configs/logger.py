import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from rich.logging import RichHandler

# PATHS
BASE_DIR = Path.cwd()

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# LOG FORMAT
LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(filename)s:%(lineno)d | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

formatter = logging.Formatter(
    fmt=LOG_FORMAT,
    datefmt=DATE_FORMAT
)

# LOGGER SETUP
def setup_logging(debug: bool = False) -> None:
    """
    Configure application-wide logging.

    Features:
    - Rich console logging
    - Rotating file logs
    - Separate error logs
    - Optional debug logs
    - UTF-8 safe
    - Production ready
    """

    root_logger = logging.getLogger()

    # Prevent duplicated handlers
    if root_logger.handlers:
        root_logger.handlers.clear()

    root_logger.setLevel(
        logging.DEBUG if debug else logging.INFO
    )

    # CONSOLE LOGGER (RICH)
    console_handler = RichHandler(
        rich_tracebacks=True,
        show_path=False,
        markup=True,
    )

    console_handler.setLevel(
        logging.DEBUG if debug else logging.INFO
    )

    console_handler.setFormatter(formatter)

    # MAIN APPLICATION LOG
    app_handler = RotatingFileHandler(
        filename=LOG_DIR / "app.log",
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=5,
        encoding="utf-8"
    )

    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)

    # ERROR LOG
    error_handler = RotatingFileHandler(
        filename=LOG_DIR / "error.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # DEBUG LOG
    debug_handler = RotatingFileHandler(
        filename=LOG_DIR / "debug.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )

    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    # REGISTER ROOT HANDLERS
    root_logger.addHandler(console_handler)
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)

    if debug:
        root_logger.addHandler(debug_handler)

    # SPECIALIZED LOGGERS
    configure_specialized_loggers()

    # STARTUP MESSAGE
    logging.getLogger(__name__).info(
        f"Logging initialized | Logs directory: {LOG_DIR.resolve()}"
    )

# SPECIALIZED LOGGERS
def configure_specialized_loggers() -> None:
    """
    Configure dedicated loggers for critical systems.
    """

    specialized_loggers = {
        "sync": "sync.log",
        "database": "database.log",
        "network": "network.log",
    }

    for logger_name, file_name in specialized_loggers.items():

        logger = logging.getLogger(logger_name)

        logger.setLevel(logging.INFO)

        logger.propagate = True

        # Prevent duplicate handlers
        if logger.handlers:
            logger.handlers.clear()

        handler = RotatingFileHandler(
            filename=LOG_DIR / file_name,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)