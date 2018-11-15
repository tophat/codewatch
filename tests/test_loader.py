from codewatch import (
    Assertion,
    ModuleLoader,
    NodeVisitor,
)


class FirstAssertion(Assertion):
    pass


class SecondAssertion(Assertion):
    pass


class FirstVisitor(NodeVisitor):
    pass


class SecondVisitor(NodeVisitor):
    pass


def file_filter():
    pass


def directory_filter():
    pass


def create_loader():
    return ModuleLoader(__name__)


def test_loads_assertions():
    loader = create_loader()
    assert [FirstAssertion, SecondAssertion] == list(loader.assertions)


def test_loads_filters():
    loader = create_loader()
    assert [directory_filter, file_filter] == list(loader.filters)


def test_loads_visitors():
    loader = create_loader()
    assert [FirstVisitor, SecondVisitor] == list(loader.visitors)
