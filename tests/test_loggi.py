# import logging
import time
from datetime import datetime

import pytest
from pathier import Pathier

import loggi

root = Pathier(__file__).parent


@pytest.fixture(scope="module")
def logdir(tmp_path_factory) -> Pathier:
    return Pathier(tmp_path_factory.mktemp("logs"))


@pytest.fixture(scope="module")
def logname() -> str:
    return "testlog"


@pytest.fixture(scope="module")
def a_logger(logname: str, logdir: Pathier) -> loggi.Logger:
    return loggi.getLogger(logname, logdir)


def test__make_log(a_logger: loggi.Logger):
    logger = a_logger
    logger.propagate = False
    logger.setLevel(loggi.DEBUG)
    logger.debug("Debug test")
    time.sleep(1)
    logger.info("Info test")
    time.sleep(1)
    logger.warning("Warning test")
    time.sleep(1)
    logger.error("Error test")
    time.sleep(1)
    logger.critical("Critical test")


def test__load_log(logname: str, logdir: Pathier):
    logfile = f"{logname}.log"
    log = loggi.load_log(logdir / logfile)
    assert log.path == logdir / logfile
    assert log.num_events == 5
    for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        assert log.filter_levels([level]).num_events == 1
    assert log.filter_messages(["*test"], ["Warning*", "Critical*"]).num_events == 3
    log.events = log.events[::-1]
    assert log.events[0].level == "CRITICAL"
    log.chronosort()
    assert log.events[0].level == "DEBUG"
    log += log
    assert log.num_events == 10
    log.chronosort()
    assert log.events[0].date == log.events[1].date
    print()
    print(log.events[0])
    print()
    print(log)


def test__get_logpaths(a_logger: loggi.Logger, logname: str, logdir: Pathier):
    path = logdir / f"{logname}.log"
    logpaths = loggi.get_logpaths(a_logger)
    assert logpaths
    assert logpaths[0] == path


def test__get_logpath(a_logger: loggi.Logger, logname: str, logdir: Pathier):
    path = logdir / f"{logname}.log"
    logpath = loggi.get_logpath(a_logger)
    assert logpath == path


def test__get_log(a_logger: loggi.Logger):
    log = loggi.get_log(a_logger)
    assert log
    assert len(log) == 5
