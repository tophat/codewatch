from codewatch import (
    Assertion,
    Stats,
    with_stats_namespace,
)


class EmptyAssertion(Assertion):
    pass


class SuccessfulAssertion(Assertion):
    def assert_success(self):
        return True, None


class UnsuccessfulAssertion(Assertion):
    ERR_MSG = 'assertion failed!'

    def assert_fail(self):
        return False, self.ERR_MSG


class MultipleAssertions(SuccessfulAssertion, UnsuccessfulAssertion):
    pass


def test_empty_assertion():
    successes, failures = [], {}
    EmptyAssertion(Stats()).run(successes, failures)

    assert successes == []
    assert failures == {}


def test_successful_assertion():
    successes, failures = [], {}
    SuccessfulAssertion(Stats()).run(successes, failures)

    assert successes == [
        SuccessfulAssertion.__name__ +
        '.' +
        SuccessfulAssertion.assert_success.__name__
    ]
    assert failures == {}


def test_unsuccessful_assertion():
    successes, failures = [], {}
    assertion = UnsuccessfulAssertion(Stats())
    assertion.run(successes, failures)

    label = (
        UnsuccessfulAssertion.__name__ +
        '.' +
        UnsuccessfulAssertion.assert_fail.__name__
    )
    assert successes == []
    assert failures == {label: assertion.ERR_MSG}


def test_multiple_assertions():
    successes, failures = [], {}
    assertion = MultipleAssertions(Stats())
    assertion.run(successes, failures)

    success_label = (
        MultipleAssertions.__name__ +
        '.' +
        MultipleAssertions.assert_success.__name__
    )
    failure_label = (
        MultipleAssertions.__name__ +
        '.' +
        MultipleAssertions.assert_fail.__name__
    )
    assert successes == [success_label]
    assert failures == {failure_label: assertion.ERR_MSG}


def test_injects_stats():
    successes, failures = [], {}
    stats = Stats()
    stats.increment('counter')

    class StatsAssertion(Assertion):
        def assert_injects_stats(self):
            assert self.stats == stats
            assert self.stats.get('counter') == 1
            return True, None

    assertion = StatsAssertion(stats)
    assertion.run(successes, failures)


def test_with_stats_namespace():
    stats = Stats()
    namespaced_stats = stats.namespaced('level2').namespaced('level3')
    namespaced_stats.increment('counter')

    class CustomAssertion(Assertion):
        @with_stats_namespace('level2', 'level3')
        def assert_injects_stats(self):
            assert self.stats.items() == namespaced_stats.items()
            assert self.stats.get('counter') == 1
            return True, None

    assertion = CustomAssertion(stats)
    assertion.run([], {})


def test_with_stats_namespace_does_not_fail_if_empty():
    stats = Stats()

    class CustomAssertion(Assertion):
        @with_stats_namespace('level2', 'level3')
        def assert_injects_stats(self):
            assert len(self.stats.keys()) == 0
            return True, None

    assertion = CustomAssertion(stats)
    assertion.run([], {})
