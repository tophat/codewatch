import os

from codewatch import Runner

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def test_full_run():
    runner = Runner(THIS_DIR, 'config_module')
    successes, failures = runner.run()
    assert successes == [
        'MyAssertion.assert_always_true',
        'MyAssertion.assert_expressions_more_than_zero',
    ]
    assert failures == {
        'MyAssertion.assert_always_false': 'should always be false',
    }
