import ast
import uuid


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
    method_name = 'visit_' + node_name.capitalize()

    def decorator(fn):
        setattr(klass, method_name, fn)

        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapper.wrapped_node_visitor = klass
        return wrapper
    return decorator
