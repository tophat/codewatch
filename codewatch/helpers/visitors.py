import importlib

from astroid.exceptions import InferenceError
from astroid.nodes import (
    Call,
    ImportFrom,
    Import,
)

from codewatch.helpers.inference import get_inference_for_model
from codewatch.node_visitor import NodeVisitorMaster


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


def count_calls_on_model(stats_namespace, model_qname, method_name):
    def record_stats(stats, rel_file_path):
        stats = stats.namespaced(stats_namespace)
        stats.increment(rel_file_path)

    def visit_call(node, stats, rel_file_path):
        if (
            not hasattr(node.func, 'attrname')
            or node.func.attrname != method_name
        ):
            return
        if not hasattr(node.func, 'expr'):
            return

        try:
            inferred = node.func.expr.inferred()
        except InferenceError:
            return
        if inferred[0].qname() == model_qname:
            record_stats(stats, rel_file_path)

    NodeVisitorMaster.register_visitor(Call, visit_call, inferences=[
        get_inference_for_model(model_qname),
    ])
