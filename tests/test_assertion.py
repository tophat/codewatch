import pytest

from codewatch.assertion import (
    Assertion,
    assertion,
)
from codewatch.stats import Stats
from tests.mock_data import (
    MOCK_BASEEXCEPTION_CLASS,
    MOCK_ERR,
    MOCK_FAILURE_MSG,
    MOCK_LABEL,
    baseexception_assertion,
    erroring_assertion,
    label_assertion,
    stats_assertion,
    successful_assertion,
    unsuccessful_assertion,
)


def test_successful_assertion():
    successes, failures, errors = Assertion(
        Stats(),
        [successful_assertion],
    ).run()
    assert successes == [successful_assertion.__name__]
    assert failures == {}
    assert errors == {}


def test_unsuccessful_assertion():
    successes, failures, errors = Assertion(
        Stats(),
        [unsuccessful_assertion],
    ).run()
    assert successes == []
    assert failures == {unsuccessful_assertion.__name__: MOCK_FAILURE_MSG}
    assert errors == {}


def test_erroring_assertion():
    successes, failures, errors = Assertion(
        Stats(),
        [erroring_assertion],
    ).run()
    assert successes == []
    assert failures == {}
    assert errors == {erroring_assertion.__name__: MOCK_ERR}


def test_baseexception_assertion_bubbles():
    with pytest.raises(MOCK_BASEEXCEPTION_CLASS):
        Assertion(Stats(), [baseexception_assertion]).run()


def test_multiple_assertions():
    assertions = [
        successful_assertion,
        unsuccessful_assertion,
    ]
    successes, failures, errors = Assertion(Stats(), assertions).run()

    assert successes == [successful_assertion.__name__]
    assert failures == {unsuccessful_assertion.__name__: MOCK_FAILURE_MSG}


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
    successes, _, _ = Assertion(Stats(), [label_assertion]).run()
    assert successes[0] == MOCK_LABEL
