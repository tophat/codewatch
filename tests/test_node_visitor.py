import astroid
import pytest

from codewatch.node_visitor import NodeVisitor, NodeVisitorMaster, count_calling_files
from codewatch.stats import Stats


def test_sets_stats_and_file_path():
    stats = Stats()
    file_path = "/mock/path"
    node_visitor = NodeVisitor(stats, file_path)

    assert node_visitor.stats == stats
    assert node_visitor.rel_file_path == file_path


@pytest.mark.parametrize('stats_namespace,code,func_name,module_name,expected_stats', [
    (
        'COUNT_FUNCTION_CALLS',
        'function()',
        'function',
        'function_module',
        {'COUNT_FUNCTION_CALLS': {'function_module.py': 1}}
    ),
    (
        'COUNT_SIMPLE_METHOD_CALLS',
        'some_object.simple_method()',
        'simple_method',
        'simple_method_module',
        {'COUNT_SIMPLE_METHOD_CALLS': {'simple_method_module.py': 1}}
    ),
])
def test_count_calling_files_function(stats_namespace, code, func_name, module_name, expected_stats):
    module = astroid.parse(code, module_name)

    assert len(NodeVisitorMaster._node_visitors) == 0

    count_calling_files(stats_namespace, func_name, module_name)

    assert len(NodeVisitorMaster._node_visitors) == 1

    stats = Stats()
    NodeVisitorMaster.visit(stats, module, module_name + ".py")

    assert stats == expected_stats


def test_count_calling_files_simple_method():
    pass


def test_count_calling_files_nested_objects():
    pass
