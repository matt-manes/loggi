# import logging
import time

import pytest
from pathier import Pathier

import loggi

root = Pathier(__file__).parent


@pytest.fixture(scope="module")
def logdir(tmp_path_factory) -> Pathier:  # type: ignore
    return Pathier(tmp_path_factory.mktemp("logs"))  # type: ignore


@pytest.fixture(scope="module")
def logname() -> str:
    return "testlog"


@pytest.fixture(scope="module")
def a_logger(logname: str, logdir: Pathier) -> loggi.Logger:
    return loggi.getLogger(logname, logdir)


def test__subclass(a_logger: loggi.Logger):
    assert isinstance(a_logger, loggi.Logger)


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
    log = a_logger.get_log()
    assert log
    assert len(log) == 5


def test__logprint(a_logger: loggi.Logger):
    a_logger.setLevel(loggi.INFO)
    # should print
    a_logger.logprint("Yeet", loggi.INFO)
    # shouldn't print
    a_logger.logprint("YeetteeY", loggi.DEBUG)


def test__logpaths(a_logger: loggi.Logger, logname: str, logdir: Pathier):
    assert (logdir / logname).with_suffix(".log") in a_logger.logpaths


def test__logpath(a_logger: loggi.Logger, logname: str, logdir: Pathier):
    assert (logdir / logname).with_suffix(".log") == a_logger.logpath


def test__close(a_logger: loggi.Logger):
    a_logger.close()


class Dummy(loggi.LoggerMixin):
    def __init__(self):
        self.init_logger()


class Dummy2(Dummy): ...


class Dummy3(loggi.LoggerMixin):
    def __init__(self):
        self.init_logger(loggi.LogName.FILENAME)


def test__mixin():
    (Pathier.cwd() / "logs").delete()
    dummy = Dummy()
    dummy.logger.info("test")
    log = dummy.logger.get_log()
    assert log
    assert log.path == Pathier.cwd() / "logs" / "dummy.log"
    assert log.num_events == 1
    assert log.events[0].level == "INFO"
    assert log.events[0].message == "test"
    dummy.logger.close()
    dummy = Dummy2()
    dummy.logger.info("test")
    log = dummy.logger.get_log()
    assert log
    assert log.path == Pathier.cwd() / "logs" / "dummy2.log"
    dummy.logger.close()
    dummy = Dummy3()
    dummy.logger.info("test")
    log = dummy.logger.get_log()
    assert log
    assert log.path == Pathier.cwd() / "logs" / "test_loggi.log"
    dummy.logger.close()
    (Pathier.cwd() / "logs").delete()
