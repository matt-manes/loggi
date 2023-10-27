# import logging
import time
from datetime import datetime

import pytest
from pathier import Pathier

import loggi

root = Pathier(__file__).parent


@pytest.fixture(scope="module")
def logpath(tmp_path_factory) -> Pathier:
    return Pathier(tmp_path_factory.mktemp("logs"))


def test__make_log(logpath: Pathier):
    logger = loggi.getLogger("loggi", logpath)
    logger.propagate = False
    logger.info("yeet")
    assert "yeet" in (logpath / "loggi.log").read_text()


def test__load_log(logpath: Pathier):
    logger = loggi.getLogger("load", logpath)
    logger.propagate = False
    logger.setLevel(loggi.DEBUG)
    logger.debug("Debug test")
    time.sleep(1)
    time1 = datetime.now()
    time.sleep(1)
    logger.info("Info test")
    time.sleep(1)
    logger.warning("Warning test")
    time.sleep(1)
    time2 = datetime.now()
    time.sleep(1)
    logger.error("Error test")
    time.sleep(1)
    logger.critical("Critical test")
    log = loggi.load_log(logpath / "load.log")
    assert log.path == logpath / "load.log"
    assert log.num_events == 5
    for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        assert log.filter_levels([level]).num_events == 1
    assert log.filter_dates(time1, time2).num_events == 2
    assert log.filter_dates(stop=time2).num_events == 3
    assert log.filter_dates(time2).num_events == 2
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
