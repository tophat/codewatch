import importlib

from codewatch.assertion import Assertion
from codewatch.node_visitor import NodeVisitor


def _enumerate_subclasses_in_module(_module, parent_class):
    subclasses = []
    for attr_name in dir(_module):
        attr = getattr(_module, attr_name)
        if not type(attr) is type:
            continue
        if not issubclass(attr, parent_class):
            continue
        subclasses.append(attr)
    return subclasses


class ModuleLoader(object):
    def __init__(
        self,
        assertion_module_name,
        filter_module_name,
        visitor_module_name,
    ):
        self.assertion_module_name = assertion_module_name
        self.filter_module_name = filter_module_name
        self.visitor_module_name = visitor_module_name

    def load_assertions(self):
        assertion_module = importlib.import_module(self.assertion_module_name)
        return _enumerate_subclasses_in_module(assertion_module, Assertion)

    def load_file_filters(self):
        filter_module = importlib.import_module(self.filter_module_name)
        if not hasattr(filter_module, 'directory_filter'):
            raise NotImplementedError('need directory_filter method in filter_module')
        if not hasattr(filter_module, 'file_filter'):
            raise NotImplementedError('need file_filter method in filter_module')
        directory_filter = getattr(filter_module, 'directory_filter')
        file_filter = getattr(filter_module, 'file_filter')
        return directory_filter, file_filter

    def load_node_visitors(self):
        node_visitor_module = importlib.import_module(self.visitor_module_name)
        return _enumerate_subclasses_in_module(node_visitor_module, NodeVisitor)
