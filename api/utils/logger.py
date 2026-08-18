import logging

from utils.environment import DEBUG

logger = logging.getLogger("chatbot")

if DEBUG:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
else:
    logger.addHandler(logging.NullHandler())


def debug(message, *args, **kwargs):
    if DEBUG:
        logger.debug(message, *args, **kwargs)


def info(message, *args, **kwargs):
    if DEBUG:
        logger.info(message, *args, **kwargs)


def warning(message, *args, **kwargs):
    if DEBUG:
        logger.warning(message, *args, **kwargs)


def error(message, *args, **kwargs):
    if DEBUG:
        logger.error(message, *args, **kwargs)


def exception(message, *args, **kwargs):
    if DEBUG:
        logger.exception(message, *args, **kwargs)
