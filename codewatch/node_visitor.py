from astroid.transforms import TransformVisitor
from functools import wraps


class NodeVisitor(TransformVisitor):
    def __init__(self, stats, rel_file_path):
        self.stats = stats
        self.rel_file_path = rel_file_path
        super(NodeVisitor, self).__init__()

    def _transform(self, node):
        cls = node.__class__
        if cls not in self.transforms:
            # no transform registered for this class of node
            return node
        node._stats = self.stats
        node._rel_file_path = self.rel_file_path
        return super(NodeVisitor, self)._transform(node)


def visit(node):
    def decorator(fn):
        @wraps(fn)
        def wrapper(node, *args, **kwargs):
            return fn(node, node._stats, node._rel_file_path, *args, **kwargs)
        wrapper._wrapper_node = node
        return wrapper
    return decorator


class NodeVisitorMaster(object):
    def __init__(self, loader, stats):
        self.stats = stats
        self.node_visitors = loader.visitors

    @staticmethod
    def load_visitors(module):
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if hasattr(attr, '_wrapper_node'):
                yield attr

    def _initialize_node_visitors(self, rel_file_path):
        initialized_node_visitors = []
        for node_visitor in self.node_visitors:
            node_visitor_obj = NodeVisitor(self.stats, rel_file_path)
            node_visitor_obj.register_transform(
                node_visitor._wrapper_node,
                node_visitor,
            )
            initialized_node_visitors.append(node_visitor_obj)
        return initialized_node_visitors

    def visit(self, node, rel_file_path):
        node_visitors_initialized = self._initialize_node_visitors(
            rel_file_path,
        )

        for node_visitor_initialized in node_visitors_initialized:
            node_visitor_initialized.visit(node)
