import importlib
from collections import namedtuple
from functools import wraps

from astroid import inference_tip
from astroid.nodes import (
    Call,
    ImportFrom,
    Import,
)
from astroid.node_classes import NodeNG
from astroid.exceptions import InferenceError
from astroid.transforms import TransformVisitor


Inference = namedtuple('Inference', ('node', 'fn', 'predicate'))
CodewatchNodeAnnotations = namedtuple(
    "CodewatchNodeAnnotations", ["stats", "rel_file_path"]
)


class NodeVisitor(TransformVisitor):
    def __init__(self, stats, rel_file_path):
        self.stats = stats
        self.rel_file_path = rel_file_path
        super(NodeVisitor, self).__init__()

    def _add_codewatch_annotations(self, node):
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


def inference(node, fn, predicate=None):
    return Inference(node, fn, predicate)


def visit(node_type, predicate=None, inferences=None):
    def decorator(fn):
        NodeVisitorMaster.register_visitor(
            node_type, fn, predicate, inferences,
        )
        return fn

    return decorator


def count_import_usages(stats_namespace, expected_qname, importer=None):
    if importer is None:
        importer = importlib.import_module

    module_name = '.'.join(expected_qname.split('.')[:-1])
    trouble_attribute = expected_qname.split('.')[-1]

    def track_import(stats, rel_file_path):
        stats.namespaced(stats_namespace).increment(rel_file_path)

    def visit_import(import_node, stats, rel_file_path):
        for name, alias in import_node.names:
            if name == expected_qname:
                track_import(stats, rel_file_path)
        return import_node

    def visit_importfrom(import_from_node, stats, rel_file_path):
        modname = import_from_node.modname

        for name, alias in import_from_node.names:
            if name == '*':
                module = importer(module_name)
                if trouble_attribute in dir(module):
                    track_import(stats, rel_file_path)
            else:
                imported_qname = modname + '.' + name
                if imported_qname == expected_qname:
                    track_import(stats, rel_file_path)
        return import_from_node

    NodeVisitorMaster.register_visitor(Import, visit_import, None)
    NodeVisitorMaster.register_visitor(ImportFrom, visit_importfrom, None)


def count_calling_files(
    stats_namespace,
    expected_callable_qname,
    inferences=None,
):
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

    NodeVisitorMaster.register_visitor(Call, visit_call, inferences=inferences)


class NodeVisitorMaster(object):
    node_visitor_registry = []

    @classmethod
    def register_visitor(
        cls,
        node,
        visitor_function,
        predicate=None,
        inferences=None,
    ):
        wrapped = _astroid_interface_for_visitor(visitor_function)

        if not issubclass(node, NodeNG):
            raise Exception(
                "visitor_function registered for invalid node type. "
                "Please use a NodeNG subclass from the astroid.nodes module."
            )

        cls.node_visitor_registry.append(
            (node, wrapped, predicate, inferences)
        )

    @classmethod
    def _initialize_node_visitors(cls, stats, rel_file_path):
        initialized_node_visitors = []
        for (
            node,
            node_visitor_function,
            predicate,
            inferences,
        ) in cls.node_visitor_registry:
            node_visitor_obj = NodeVisitor(stats, rel_file_path)

            if inferences is not None:
                for inference in inferences:
                    node_visitor_obj.register_transform(
                        inference.node,
                        inference_tip(inference.fn),
                        inference.predicate,
                    )

            node_visitor_obj.register_transform(
                node,
                node_visitor_function,
                predicate,
            )
            initialized_node_visitors.append(node_visitor_obj)
        return initialized_node_visitors

    @classmethod
    def visit(cls, stats, node, rel_file_path):
        node_visitors_initialized = cls._initialize_node_visitors(
            stats, rel_file_path
        )

        for node_visitor_initialized in node_visitors_initialized:
            node_visitor_initialized.visit(node)
