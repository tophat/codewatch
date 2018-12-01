import os
import sys
from subprocess import call

from tests.config_modules import (
    integration_config,
    integration_config_utf8,
)


def _call_codewatch(pargs, **kwargs):
    pythonexec = sys.executable or 'python'
    codewatchbin = os.path.normcase('./bin/codewatch')
    return call([pythonexec, codewatchbin] + pargs, shell=True, **kwargs) & 0xFF


def test_codewatch_returns_success():
    ret = _call_codewatch([integration_config.__name__])
    assert ret == 255


def test_codewatch_utf8_returns_success():
    ret = _call_codewatch([integration_config_utf8.__name__])
    assert ret == 0
