import astroid
import pytest

from codewatch.node_visitor import (
    NodeVisitor,
    NodeVisitorMaster,
    count_calling_files,
)
from codewatch.stats import Stats


def test_sets_stats_and_file_path():
    stats = Stats()
    file_path = "/mock/path"
    node_visitor = NodeVisitor(stats, file_path)

    assert node_visitor.stats == stats
    assert node_visitor.rel_file_path == file_path


@pytest.mark.parametrize(
    "stats_namespace,code,module_name,expected_callable_qname,expected_stats",
    [
        (
            "COUNT_FUNCTION_CALLS",
            """
def function():
    pass
function()""",
            "function_module",
            "function_module.function",
            {"COUNT_FUNCTION_CALLS": {"function_module.py": 1}},
        ),
        (
            "COUNT_SIMPLE_METHOD_CALLS",
            """\
class SomeClass(object):
    @staticmethod
    def simple_method(self):
            pass
SomeClass.simple_method()""",
            "simple_method_module",
            "simple_method_module.SomeClass.simple_method",
            {"COUNT_SIMPLE_METHOD_CALLS": {"simple_method_module.py": 1}},
        ),
        (
            "COUNT_NESTED_METHOD_CALLS",
            """\
class InnerClass(object):
    def inner_method(self):
        pass

class OuterClass(object):
    def outer_method(self):
        return InnerClass()
OuterClass.outer_method().inner_method()""",
            "nested_method_module",
            "nested_method_module.InnerClass.inner_method",
            {"COUNT_NESTED_METHOD_CALLS": {"nested_method_module.py": 1}},
        ),
    ],
)
def test_count_calling_files_function(
    stats_namespace, code, module_name, expected_callable_qname, expected_stats
):
    NodeVisitorMaster.node_visitor_registry = []

    module = astroid.parse(code, module_name)

    assert len(NodeVisitorMaster.node_visitor_registry) == 0

    count_calling_files(stats_namespace, expected_callable_qname)

    assert len(NodeVisitorMaster.node_visitor_registry) == 1

    stats = Stats()
    NodeVisitorMaster.visit(stats, module, module_name + ".py")

    assert stats == expected_stats
