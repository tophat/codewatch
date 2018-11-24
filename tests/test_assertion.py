from codewatch.assertion import (
    Assertion,
    assertion,
)
from codewatch.stats import Stats
from tests.mock_data import ERR_MSG, MOCK_LABEL, successful_assertion, unsuccessful_assertion, stats_assertion, \
    label_assertion


def test_successful_assertion():
    successes, failures = Assertion(Stats(), [successful_assertion]).run()
    assert successes == [successful_assertion.__name__]
    assert failures == {}


def test_unsuccessful_assertion():
    successes, failures = Assertion(Stats(), [unsuccessful_assertion]).run()
    assert successes == []
    assert failures == {unsuccessful_assertion.__name__: ERR_MSG}


def test_multiple_assertions():
    assertions = [
        successful_assertion,
        unsuccessful_assertion,
    ]
    successes, failures = Assertion(Stats(), assertions).run()

    assert successes == [successful_assertion.__name__]
    assert failures == {unsuccessful_assertion.__name__: ERR_MSG}


def test_injects_stats():
    stats = Stats()
    stats.increment('counter')
    Assertion(stats, [stats_assertion]).run()


def test_with_stats_namespace():
    _stats = Stats()
    namespaced_stats = _stats.namespaced('level2').namespaced('level3')
    namespaced_stats.increment('counter')

    def stats_namespaced_assertion(stats):
        assert stats.items() == namespaced_stats.items()
        assert stats.get('counter') == 1
        return True, None
    decorated_assertion = assertion(stats_namespaces=['level2', 'level3'])(
        stats_namespaced_assertion,
    )
    Assertion(_stats, [decorated_assertion]).run()


def test_label_assertion():
    successes, failures = Assertion(Stats(), [label_assertion]).run()
    assert successes[0] == MOCK_LABEL
