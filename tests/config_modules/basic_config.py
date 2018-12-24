from astroid import nodes

from codewatch.assertion import assertion
from codewatch.helpers.visitor import visit


@assertion()
def first_assertion(_stats):
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
