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
    successes, failures, errors = _get_runner_for_config(
        integration_config).run()
    assert successes == [
        'custom_label_always_true',
        'correctly_rewritten_inference',
        'expressions_more_than_zero',
        'import_from_inference_worked',
        'import_inference_worked',
        'num_import_from_more_than_zero',
        'predicate_inference_works',
        'predicate_works',
    ]
    assert failures == {
        'always_false': 'should always be false',
    }
    assert errors == {}


def test_full_run_utf8():
    successes, failures, errors = _get_runner_for_config(
        integration_config_utf8).run()
    assert successes == [
        'unicode_works'
    ]
    assert failures == {}
    assert errors == {}
