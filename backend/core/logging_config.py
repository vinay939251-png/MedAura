import logging
import sys

def setup_logging(level=logging.INFO):
    """
    Sets up structured logging for the application.
    Replaces print statements with standardized logs.
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)

    # Avoid duplicate logs if run multiple times
    if not logger.handlers:
        logger.addHandler(ch)

    return logger
