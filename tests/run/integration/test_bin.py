from subprocess import call

from tests.config_modules import (
    integration_config,
    integration_config_utf8,
    codewatch_config
)


def test_codewatch_returns_success():
    ret = call(['codewatch', integration_config.__name__])
    assert ret == 255


def test_codewatch_utf8_returns_success():
    ret = call(['codewatch', integration_config_utf8.__name__])
    assert ret == 0

def test_codewatch_config_returns_success():
    ret = call(['codewatch', codewatch_config.__name__])
    assert ret == 255
