import astroid
import pytest

from codewatch.node_visitor import (
    NodeVisitor,
    NodeVisitorMaster,
    count_calling_files,
)
from codewatch.stats import Stats


FUNCTION_CALL_CODE = """\
def function():
    pass
function()"""

SIMPLE_METHOD_CODE = """\
class SomeClass(object):
    @staticmethod
    def simple_method(self):
            pass
SomeClass.simple_method()"""

NESTED_METHOD_CODE = """\
class InnerClass(object):
    def inner_method(self):
        pass

class OuterClass(object):
    def outer_method(self):
        return InnerClass()
OuterClass.outer_method().inner_method()"""

NESTED_METHOD_IN_ATTR_CODE = """\
class InnerClass2(object):
    def inner_method(self):
        pass

class OuterClass2(object):
    inner = InnerClass2()
OuterClass2.inner.inner_method()"""


@pytest.mark.parametrize(
    "stats_namespace,code,module_name,expected_callable_qname,expected_stats",
    [
        (
            "COUNT_FUNCTION_CALLS",
            FUNCTION_CALL_CODE,
            "function_module",
            "function_module.function",
            {"COUNT_FUNCTION_CALLS": {"function_module.py": 1}},
        ),
        (
            "COUNT_SIMPLE_METHOD_CALLS",
            SIMPLE_METHOD_CODE,
            "simple_method_module",
            "simple_method_module.SomeClass.simple_method",
            {"COUNT_SIMPLE_METHOD_CALLS": {"simple_method_module.py": 1}},
        ),
        (
            "COUNT_NESTED_METHOD_CALLS",
            NESTED_METHOD_CODE,
            "nested_method_module",
            "nested_method_module.InnerClass.inner_method",
            {"COUNT_NESTED_METHOD_CALLS": {"nested_method_module.py": 1}},
        ),
        (
            "COUNT_NESTED_METHOD_IN_ATTR_CALLS",
            NESTED_METHOD_IN_ATTR_CODE,
            "nested_method_in_attr_module",
            "nested_method_in_attr_module.InnerClass2.inner_method",
            {
                "COUNT_NESTED_METHOD_IN_ATTR_CALLS": {
                    "nested_method_in_attr_module.py": 1
                }
            },
        ),
        (
            "COUNT_CHAINED_FUNCTION_CALLS",
            """
def function1():
    pass
def function2():
    return function1
function2()()""",
            "function_module",
            "function_module.function2",
            {'COUNT_CHAINED_FUNCTION_CALLS': {'function_module.py': 1}},
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


def test_sets_stats_and_file_path():
    stats = Stats()
    file_path = "/mock/path"
    node_visitor = NodeVisitor(stats, file_path)

    assert node_visitor.stats == stats
    assert node_visitor.rel_file_path == file_path
