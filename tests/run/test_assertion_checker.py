from codewatch import (
    Assertion,
    AssertionChecker,
    Stats,
)


class MockLoader(object):
    def __init__(self, assertions):
        self.assertions = assertions


class MyAssertionClass(Assertion):
    err_msg = 'my assertion failed!'

    def assert_fail_if_counter_over_5(self):
        return self.stats.get('counter', 0) > 5, self.err_msg

    def assert_always_fails(self):
        return False, self.err_msg

    def assert_always_passes(self):
        return True, None


def test_assertions_are_run_counter_check_fails():
    loader = MockLoader(assertions=[MyAssertionClass])
    stats = Stats()
    checker = AssertionChecker(loader, stats)
    successes, failures = checker.run()

    assert len(successes) == 1
    assert len(failures) == 2


def test_asserts_are_run_counter_check_passes():
    loader = MockLoader(assertions=[MyAssertionClass])
    stats = Stats()
    stats.append('counter', 10)
    checker = AssertionChecker(loader, stats)
    successes, failures = checker.run()

    assert len(successes) == 2
    assert len(failures) == 1
