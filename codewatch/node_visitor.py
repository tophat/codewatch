from collections import namedtuple
from functools import wraps

from astroid import inference_tip
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
            "CodewatchNodeAnnotations", ["stats", "rel_file_path"]
        )
        node._codewatch = CodewatchNodeAnnotations(
            self.stats, self.rel_file_path
        )
        return node

    def _transform(self, node):
        cls = node.__class__
        if cls not in self.transforms:
            # no transform registered for this class of node
            return node
        annotated_node = self._add_codewatch_annotations(node)
        return super(NodeVisitor, self)._transform(annotated_node)


def _astroid_interface_for_visitor(visitor_function):
    """Turn codewatch visitors into astroid-compatible transform functions

    codewatch visitors can make use of 3 args, the node, stats, and the
    relative file path you were visited for

    astroid transforms must take only the node

    By annotating the node with stats and relative file path, we can make our
    codewatch visitors compatible with astroid transform functions.
    """

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


def visit(node_type, change_node_inference=None):
    def decorator(fn):
        NodeVisitorMaster.register_visitor(
            node_type, fn, change_node_inference
        )
        return fn

    return decorator


def count_calling_files(stats_namespace, expected_callable_qname):
    if stats_namespace is None:
        raise Exception("count_calling_files() requires a valid namespace")

    expected_callable_name = expected_callable_qname.split(".")[-1]

    def record_stats(stats, rel_file_path):
        stats = stats.namespaced(stats_namespace)
        stats.increment(rel_file_path)

    def visit_call(call_node, stats, rel_file_path):
        """A visitor function to gather call stats.

        astroid.nodes.Call nodes are from one of two forms:
          symbol()
        or
          some.expression.attribute()

        AST are structured differently in each case. We detect and handle both.
        """
        callable_as_attribute = hasattr(call_node.func, "attrname")
        if callable_as_attribute:
            callable_name = call_node.func.attrname
        else:
            if not hasattr(call_node.func, "name"):
                return call_node
            callable_name = call_node.func.name

        # Optimization: Start with a cheap guard before astroid inference
        if callable_name != expected_callable_name:
            return call_node

        try:
            inferred_types = call_node.func.inferred()
        except InferenceError:
            return call_node

        found_matching_inferred_qname = any(
            inferred_type.qname() == expected_callable_qname
            for inferred_type in inferred_types
        )

        if not found_matching_inferred_qname:
            return call_node

        record_stats(stats, rel_file_path)

        return call_node

    NodeVisitorMaster.register_visitor(CallNode, visit_call, None)


class NodeVisitorMaster(object):
    node_visitor_registry = []

    @classmethod
    def register_visitor(
        cls, node, visitor_function, change_node_inference=None
    ):
        wrapped = _astroid_interface_for_visitor(visitor_function)

        if not issubclass(node, NodeNG):
            raise Exception(
                "visitor_function {v} registered for invalid node type. "
                "Please use a NodeNG subclass from the astroid.nodes module."
            )

        cls.node_visitor_registry.append(
            (node, wrapped, change_node_inference)
        )

    @classmethod
    def _initialize_node_visitors(cls, stats, rel_file_path):
        initialized_node_visitors = []
        for (
            node,
            node_visitor_function,
            change_node_inference,
        ) in cls.node_visitor_registry:
            node_visitor_obj = NodeVisitor(stats, rel_file_path)

            if change_node_inference is not None:
                node_visitor_obj.register_transform(
                    node, inference_tip(change_node_inference)
                )

            node_visitor_obj.register_transform(node, node_visitor_function)
            initialized_node_visitors.append(node_visitor_obj)
        return initialized_node_visitors

    @classmethod
    def visit(cls, stats, node, rel_file_path):
        node_visitors_initialized = cls._initialize_node_visitors(
            stats, rel_file_path
        )

        for node_visitor_initialized in node_visitors_initialized:
            node_visitor_initialized.visit(node)
