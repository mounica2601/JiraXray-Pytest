from jira.plugin import xray


@xray("SAM-1")
def test_sum():
    sum = 10+5
    assert sum == 15

@xray("SAM-2")
def test_sub():
    sub = 10 - 5
    assert sub == 10
