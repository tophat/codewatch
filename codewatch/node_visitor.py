import ast
import uuid
from functools import wraps


class NodeVisitor(ast.NodeVisitor):
    def __init__(self, stats, rel_file_path):
        self.stats = stats
        self.rel_file_path = rel_file_path

    @staticmethod
    def load_visitors(module):
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if hasattr(attr, 'wrapped_node_visitor'):
                yield attr.wrapped_node_visitor
                continue
            if not type(attr) is type:
                continue
            if not issubclass(attr, NodeVisitor):
                continue
            if attr == NodeVisitor:
                continue
            yield attr


def visit(node_name):
    class_name = 'NodeVisitor_' + uuid.uuid4().hex
    klass = type(class_name, (NodeVisitor,), {})
    normalized_node_name = node_name[0].upper() + node_name[1:]
    method_name = 'visit_' + normalized_node_name

    def decorator(fn):
        setattr(klass, method_name, fn)

        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapper.wrapped_node_visitor = klass
        return wrapper
    return decorator
