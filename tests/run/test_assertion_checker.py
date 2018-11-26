from codewatch.assertion import assertion
from codewatch.run import AssertionChecker
from codewatch.stats import Stats


class MockLoader(object):
    def __init__(self, assertions):
        self.assertions = assertions


@assertion()
def assert_fail_if_counter_over_5(stats):
    assert stats.get('counter', 0) > 5, 'counter is over 5'


@assertion()
def assert_always_fails(_stats):
    assert False, 'this should always fail'


@assertion()
def assert_always_passes(_stats):
    assert True


@assertion()
def assert_raise_error(_stats):
    raise KeyError(0)


ASSERTIONS = [
    assert_fail_if_counter_over_5,
    assert_always_fails,
    assert_always_passes,
    assert_raise_error,
]


def test_assertions_are_run_counter_check_fails():
    loader = MockLoader(assertions=ASSERTIONS)
    stats = Stats()
    checker = AssertionChecker(loader, stats)
    successes, failures, errors = checker.run()

    assert len(successes) == 1
    assert len(failures) == 2
    assert len(errors) == 1


def test_asserts_are_run_counter_check_passes():
    loader = MockLoader(assertions=ASSERTIONS)
    stats = Stats()
    stats.append('counter', 10)
    checker = AssertionChecker(loader, stats)
    successes, failures, errors = checker.run()

    assert len(successes) == 2
    assert len(failures) == 1
    assert len(errors) == 1
