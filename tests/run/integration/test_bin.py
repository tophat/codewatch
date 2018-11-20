from subprocess import call

from tests.run.integration import (
    config_module,
    config_module_utf8,
)


def test_codewatch_returns_success():
    ret = call(['codewatch', config_module.__name__])
    assert ret == 0


def test_codewatch_utf8_returns_success():
    ret = call(['codewatch', config_module_utf8.__name__])
    assert ret == 0
