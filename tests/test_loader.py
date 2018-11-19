from astroid import nodes
from codewatch.assertion import assertion
from codewatch.loader import ModuleLoader
from codewatch.node_visitor import visit


@assertion()
def first__assertion(_stats):
    pass


@assertion()
def second_assertion(_stats):
    pass


@visit(nodes.Import)
def my_visitor(_self):
    pass


def file_filter():
    pass


def directory_filter():
    pass


def create_loader():
    return ModuleLoader(__name__)


def test_loads_assertions():
    loader = create_loader()
    assert [first__assertion, second_assertion] == list(loader.assertions)


def test_loads_filters():
    loader = create_loader()
    assert [directory_filter, file_filter] == list(loader.filters)


def test_loads_visitors():
    loader = create_loader()
    assert next(loader.visitors) == my_visitor
