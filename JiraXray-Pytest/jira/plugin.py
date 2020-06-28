import json
import pytest

from jira.jiratasks import update_test_status, create_JIRA_Task_and_add_label

PYTEST_TO_XRAY = {
    "passed": "PASS",
    "failed": "FAIL",
    "skipped": "ABORTED"
}

XRAY_PREFIX = 'xray'


def xray(*ids):
    return pytest.mark.xray(ids=ids)


def get_test_outcome(outcome):
    return PYTEST_TO_XRAY[outcome]


def config():
    with open('resources/jiraconfig.json') as config_file:
        data = json.load(config_file)
    return data


class PytestXrayPlugin(object):
    def __init__(self):
        value = config()
        self.server = value["url"]

    @pytest.hookimpl(trylast=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        value = config()
        outcome = yield
        rep = outcome.get_result()
        if item.get_closest_marker(XRAY_PREFIX):
            testcaseids = item.get_closest_marker(XRAY_PREFIX).kwargs.get('ids')
            if rep.when == 'call' and testcaseids:
                for testcase in testcaseids:
                    if rep.outcome == "failed":
                        testcaseName = item.nodeid
                        excinfo = call.excinfo
                        description = excinfo
                        if value["globalJiraSwitchKey"]:
                            update_test_status(value["url"], value["username"], value["password"], testcase, PYTEST_TO_XRAY[outcome.get_result().outcome], value["testExecutionKey"])
                            if value["createNewJiraTasks"]:
                                create_JIRA_Task_and_add_label(value["url"], value["username"], value["password"], value["project"], testcase, str(description), testcaseName)
                    if rep.outcome == "passed":
                        if value["globalJiraSwitchKey"]:
                            update_test_status(value["url"], value["username"], value["password"], testcase, PYTEST_TO_XRAY[outcome.get_result().outcome], value["testExecutionKey"])