import os

from codewatch.run import Runner

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def test_full_run():
    runner = Runner(THIS_DIR, 'config_module')
    successes, failures = runner.run()
    assert successes == [
        'custom_label_always_true',
        'expressions_more_than_zero',
        'num_import_from_more_than_zero',
    ]
    assert failures == {
        'always_false': 'should always be false',
    }
