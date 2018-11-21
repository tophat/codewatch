from codewatch.loader import ModuleLoader
from tests.config_modules import basic_config, empty_config
from tests.config_modules.basic_config import (
    first_assertion,
    second_assertion,
    directory_filter,
    file_filter,
)


def create_loader(config=basic_config):
    return ModuleLoader(config.__name__)


def test_loads_assertions():
    loader = create_loader()
    assert [first_assertion, second_assertion] == loader.assertions


def test_loads_filters():
    loader = create_loader()
    assert (directory_filter, file_filter) == loader.filters


def test_empty_config_uses_default_filters():
    loader = create_loader(empty_config)
    assert len(loader.filters) == 2
