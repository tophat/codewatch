from codewatch.assertion import assertion
from codewatch.loader import ModuleLoader
from codewatch.node_visitor import (
    NodeVisitor,
    visit,
)


@assertion()
def first__assertion(_stats):
    pass


@assertion()
def second_assertion(_stats):
    pass


class FirstVisitor(NodeVisitor):
    pass


@visit(node_name='import')
def second_visitor(_self):
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

    assert next(loader.visitors) == FirstVisitor
    assert next(loader.visitors) == second_visitor.wrapped_node_visitor
