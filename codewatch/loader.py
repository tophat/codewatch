import importlib

from codewatch.assertion import Assertion
from codewatch.node_visitor import NodeVisitor


def _enumerate_subclasses_in_module(module, parent_class):
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if not type(attr) is type:
            continue
        if not issubclass(attr, parent_class):
            continue
        yield attr


class ModuleLoader(object):
    def __init__(
        self,
        assertion_module_name,
        filter_module_name,
        visitor_module_name,
    ):
        self.assertions = self.load_assertions(assertion_module_name)
        self.filters = self.load_file_filters(filter_module_name)
        self.visitors = self.load_node_visitors(visitor_module_name)

    def load_assertions(self, assertion_module_name):
        assertion_module = importlib.import_module(assertion_module_name)
        return _enumerate_subclasses_in_module(assertion_module, Assertion)

    def load_file_filters(self, filter_module_name):
        filter_module = importlib.import_module(filter_module_name)
        if not hasattr(filter_module, 'directory_filter'):
            raise NotImplementedError('need directory_filter method in filter_module')
        if not hasattr(filter_module, 'file_filter'):
            raise NotImplementedError('need file_filter method in filter_module')
        directory_filter = getattr(filter_module, 'directory_filter')
        file_filter = getattr(filter_module, 'file_filter')

        yield directory_filter
        yield file_filter

    def load_node_visitors(self, visitor_module_name):
        node_visitor_module = importlib.import_module(visitor_module_name)
        return _enumerate_subclasses_in_module(node_visitor_module, NodeVisitor)
