from jira.plugin import xray


@xray("SAM-1")
def test_basic_login():
    assert 10 == 5

@xray("SAM-2")
def test_sub():
    assert 10 == 10
