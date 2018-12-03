import os
import sys
from subprocess import call

from tests.config_modules import (
    integration_config,
    integration_config_utf8,
    codewatch_config
)


def _call_codewatch(pargs, **kwargs):
    bargs = []
    if sys.platform == "win32":
        bargs.append(sys.executable or "python")
        bargs.append(os.path.normcase("./bin/codewatch"))
        kwargs.update(shell=True)
    else:
        bargs.append("codewatch")
    return call(bargs + pargs, **kwargs) & 0xFF


def test_codewatch_returns_correct_exit_code():
    ret = _call_codewatch([integration_config.__name__])
    assert ret == 255


def test_codewatch_utf8_returns_success():
    ret = _call_codewatch([integration_config_utf8.__name__])
    assert ret == 0

def test_codewatch_config_returns_success():
    ret = _call_codewatch(['codewatch', codewatch_config.__name__])
    assert ret == 255
