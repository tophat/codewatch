from codewatch import assertion

ERR_MSG = 'assertion failed!'
MOCK_LABEL = 'wow_nice_label'


@assertion()
def successful_assertion(_stats):
    pass


@assertion()
def unsuccessful_assertion(_stats):
    assert False, ERR_MSG


@assertion()
def stats_assertion(stats):
    assert stats == stats
    assert stats.get('counter') == 1


@assertion(label=MOCK_LABEL)
def label_assertion(_stats):
    pass
