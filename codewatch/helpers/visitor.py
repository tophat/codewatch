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
    """
    Functions decorated with `visit` are called on nodes of type `node_type`
    eg: To count the number of imports in each file

    @visit('import')
    def my_visitor(node, stats, rel_file_path):
        stats['imports'].increment(rel_file_path)
    """
    def decorator(fn):
        NodeVisitorMaster.register_visitor(
            node_type, fn, predicate, inferences,
        )
        return fn

    return decorator


def _validate_stats_namespace(fn_name, stats_namespace):
    if stats_namespace is None:
        raise Exception("{} requires a valid namespace".format(fn_name))


def count_import_usages(stats_namespace, expected_qname, importer=None):
    """
    A visitor to track the number of times a particular attribute is imported
    eg: To track the number of times the User model is imported

    count_import_usages('imports_num_user_model', 'app.models.User')
    """
    _validate_stats_namespace('count_import_usages', stats_namespace)
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
            if name == '*' and module_name == modname:
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
    _validate_stats_namespace('count_calling_files', stats_namespace)
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


def count_calls_on_django_model(stats_namespace, model_qname, method_name):
    """
    Counts the number of times a particular method is called on a Django model
    Populates stats with the number of calls per file

    eg:
    count_calls_on_django_model(
      'destroy_calls', 'app.lobby.models.User', 'destroy')

    stats => {'destroy_calls': {'app/lobby/views.py': 15}}

    This indicates the the destroy() function was called 15 times on the
    User model in app/lobby/views.py
    """
    _validate_stats_namespace('count_calls_on_django_model', stats_namespace)

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
            inferred = next(node.func.expr.infer())
        except InferenceError:
            return
        if hasattr(inferred, 'qname') and inferred.qname() == model_qname:
            record_stats(stats, rel_file_path)

    NodeVisitorMaster.register_visitor(Call, visit_call, inferences=[
        get_inference_for_model(model_qname),
    ])
