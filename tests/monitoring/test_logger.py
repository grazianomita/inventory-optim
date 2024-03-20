import logging

from inventory_optim.monitoring.logger import create_logger


def test_create_logger():
    logger = create_logger(logging.INFO)
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)
    assert logger.handlers[0].level == logging.INFO
    formatter = logger.handlers[0].formatter
    assert isinstance(formatter, logging.Formatter)
    assert formatter._fmt == '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
