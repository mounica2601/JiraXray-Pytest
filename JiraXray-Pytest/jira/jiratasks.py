import json

import requests


def create_JIRA_Task_and_add_label(url, username, password, projectkey, testcaseID, description, testcasename):
    body = {
        "fields": {
            "project":
                {
                    "key": projectkey
                },
            "summary": "Automation  Failure Task with the test case in the suite "+testcasename,
            "description": description,
            "issuetype": {
                "name": "Task"
            }
        },
        "update": {
            "issuelinks": [
                {
                    "add": {
                        "type": {
                            "name": "Blocks",
                            "inward": "is blocked by",
                            "outward": "blocks"
                        },
                        "outwardIssue": {
                            "key": testcaseID
                        }
                    }
                }
            ]
        }
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post(url+"/rest/api/2/issue/", data=json.dumps(body), headers=headers,
                      auth=(username, password))

    json_data = r.json()
    taskid = json_data['key']
    print(taskid)

    labelbody = {
        "update": {"labels": [{"add": "Automation"}]}
    }
    headers = {"Content-Type": "application/json"}
    r = requests.put(url + "/rest/api/2/issue/" + taskid, data=json.dumps(labelbody), headers=headers,
                     auth=(username, password))


def update_test_status(url, username, password, testcaseID, test_status, testExecutionKey):
    testdata = {
        "testExecutionKey": testExecutionKey,
        "info": {
            "summary": "Test Execution Sample",
            "description": "This execution is automatically created when importing execution results from an external source",
            "user": username
        },
        "tests": [

        ]
    }
    mylist = []
    mylist.append({'comment': 'Successful execution', 'status': test_status, 'testKey': testcaseID})
    testdata.update({'tests': mylist})

    headers = {"Content-Type": "application/json"}
    r = requests.post(url+"/rest/raven/1.0/import/execution/",
                      data=json.dumps(testdata), headers=headers,
                      auth=(username, password))