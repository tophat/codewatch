from codewatch.assertion import assertion
from codewatch.run import AssertionChecker
from codewatch.stats import Stats


class MockLoader(object):
    def __init__(self, assertions):
        self.assertions = assertions


@assertion()
def assert_fail_if_counter_over_5(stats):
    return stats.get('counter', 0) > 5, 'counter is over 5'


@assertion()
def assert_always_fails(_stats):
    return False, 'this should always fail'


@assertion()
def assert_always_passes(_stats):
    return True, None


ASSERTIONS = [
    assert_fail_if_counter_over_5,
    assert_always_fails,
    assert_always_passes,
]


def test_assertions_are_run_counter_check_fails():
    loader = MockLoader(assertions=ASSERTIONS)
    stats = Stats()
    checker = AssertionChecker(loader, stats)
    successes, failures = checker.run()

    assert len(successes) == 1
    assert len(failures) == 2


def test_asserts_are_run_counter_check_passes():
    loader = MockLoader(assertions=ASSERTIONS)
    stats = Stats()
    stats.append('counter', 10)
    checker = AssertionChecker(loader, stats)
    successes, failures = checker.run()

    assert len(successes) == 2
    assert len(failures) == 1
