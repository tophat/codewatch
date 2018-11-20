import os

from codewatch.run import Runner
from tests.config_modules import (
    integration_config,
    integration_config_utf8,
)


def _get_runner_for_config(config):
    file_path = os.path.abspath(config.__file__)
    base_dir = os.path.dirname(file_path)

    file_name = os.path.basename(file_path)
    file_name_wo_ext = os.path.splitext(file_name)[0]
    return Runner(base_dir, file_name_wo_ext)


def test_full_run():
    successes, failures = _get_runner_for_config(integration_config).run()
    assert successes == [
        'custom_label_always_true',
        'expressions_more_than_zero',
        'num_import_from_more_than_zero',
    ]
    assert failures == {
        'always_false': 'should always be false',
    }


def test_full_run_utf8():
    successes, failures = _get_runner_for_config(integration_config_utf8).run()
    assert successes == [
        'unicode_works'
    ]
    assert failures == {}
