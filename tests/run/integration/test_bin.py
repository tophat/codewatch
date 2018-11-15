from subprocess import call

from tests.run.integration import config_module


def test_codewatch_returns_success():
    ret = call(['codewatch', config_module.__name__])
    assert ret == 0
