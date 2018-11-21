from collections import namedtuple
from functools import partial, wraps

from astroid.nodes import Call as CallNode
from astroid.node_classes import NodeNG
from astroid.exceptions import InferenceError
from astroid.transforms import TransformVisitor


class NodeVisitor(TransformVisitor):
    def __init__(self, stats, rel_file_path):
        self.stats = stats
        self.rel_file_path = rel_file_path
        super(NodeVisitor, self).__init__()

    def _add_codewatch_annotations(self, node):
        CodewatchNodeAnnotations = namedtuple(
            'CodewatchNodeAnnotations',
            ['stats', 'rel_file_path']
        )
        node._codewatch = CodewatchNodeAnnotations(self.stats, self.rel_file_path)
        return node

    def _transform(self, node):
        cls = node.__class__
        if cls not in self.transforms:
            # no transform registered for this class of node
            return node
        annotated_node = self._add_codewatch_annotations(node)
        return super(NodeVisitor, self)._transform(annotated_node)


def _astroid_interface_for_visitor(visitor_function):
    '''Turn codewatch visitors into astroid-compatible transform functions

    codewatch visitors can make use of 3 args, the node, stats, and the
    relative file path you were visited for

    astroid transforms must take only the node

    By annotating the node with stats and relative file path, we can make our
    codewatch visitors compatible with astroid transform functions.
    '''

    @wraps(visitor_function)
    def call_visitor(annotated_node, *args, **kwargs):
        return visitor_function(
            annotated_node,
            annotated_node._codewatch.stats,
            annotated_node._codewatch.rel_file_path,
            *args,
            **kwargs
        )
    return call_visitor


def visit(node_type):
    def decorator(fn):
        wrapper = _astroid_interface_for_visitor(fn)
        NodeVisitorMaster.register_visitor(node_type, wrapper)
        return wrapper
    return decorator


def count_calling_files(stats_namespace, name, module, expected_type=None):
    if stats_namespace is None:
        raise Exception("count_calling_files() requires a valid namespace")

    def record_stats(stats, rel_file_path):
        if stats_namespace is not None:
            stats = stats.namespaced(stats_namespace)
        stats.increment(rel_file_path)

    def visit_method_call(call_node, stats, rel_file_path):
        if not hasattr(call_node.func, "attrname"):
            return call_node
        if call_node.func.attrname != name:
            return call_node

        try:
            inferred_types = call_node.func.expr.inferred()
        except InferenceError:
            return call_node

        expected_python_type = ".".join([module, expected_type])

        inferred_an_expected_python_type = any(
            '.'.join([inferred_type.root().name, inferred_type.name]) == expected_python_type
            for inferred_type in inferred_types
        )

        if not inferred_an_expected_python_type:
            return call_node

        record_stats(stats, rel_file_path)

        return call_node

    def visit_function_call(call_node, stats, rel_file_path):
        if call_node.func.name != name:
            return call_node
        record_stats(stats, rel_file_path)
        return call_node


    if expected_type is None:
        visit_call = _astroid_interface_for_visitor(visit_function_call)
    else:
        visit_call = _astroid_interface_for_visitor(visit_method_call)

    NodeVisitorMaster.register_visitor(CallNode, visit_call)


class NodeVisitorMaster(object):
    node_visitor_registry = []

    @classmethod
    def register_visitor(cls, node, visitor_function):
        if not issubclass(node, NodeNG):
            raise Exception(
                "visitor_function {v} registered for invalid node type. "
                "Please use a NodeNG subclass from the astroid.nodes module."
            )

        cls.node_visitor_registry.append((node, visitor_function))

    @classmethod
    def _initialize_node_visitors(cls, stats, rel_file_path):
        initialized_node_visitors = []
        for node_visitor in cls.node_visitor_registry:
            node_visitor_obj = NodeVisitor(stats, rel_file_path)
            node_visitor_obj.register_transform(
                node_visitor[0], node_visitor[1]
            )
            initialized_node_visitors.append(node_visitor_obj)
        return initialized_node_visitors

    @classmethod
    def visit(cls, stats, node, rel_file_path):
        node_visitors_initialized = cls._initialize_node_visitors(stats, rel_file_path)

        for node_visitor_initialized in node_visitors_initialized:
            node_visitor_initialized.visit(node)
