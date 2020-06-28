import pathlib
import pytest

from jira.plugin import PytestXrayPlugin


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "report_" + report.when, report)


def pytest_configure(config):
    config.pluginmanager.register(PytestXrayPlugin())