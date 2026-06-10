import logging


def test_log_on_failure():
    logging.warning("pytest log warning")
    assert False


def test_log_on_success():
    logging.warning("pytest log warning")
