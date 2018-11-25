from codewatch import assertion

MOCK_FAILURE_MSG = 'assertion failed!'
MOCK_ERR = KeyError(0)
MOCK_BASEEXCEPTION_CLASS = KeyboardInterrupt
MOCK_LABEL = 'wow_nice_label'


@assertion()
def successful_assertion(_stats):
    pass


@assertion()
def unsuccessful_assertion(_stats):
    assert False, MOCK_FAILURE_MSG


@assertion()
def erroring_assertion(_stats):
    raise MOCK_ERR


@assertion()
def baseexception_assertion(_stats):
    raise MOCK_BASEEXCEPTION_CLASS()


@assertion()
def stats_assertion(stats):
    assert stats == stats
    assert stats.get('counter') == 1


@assertion(label=MOCK_LABEL)
def label_assertion(_stats):
    pass
