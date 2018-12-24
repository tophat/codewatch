from collections import namedtuple
from functools import wraps

from astroid import inference_tip
from astroid.node_classes import NodeNG
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
