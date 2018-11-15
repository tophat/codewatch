from codewatch.node_visitor import NodeVisitor
from codewatch.stats import Stats


def test_sets_stats_and_file_path():
    stats = Stats()
    file_path = '/mock/path'
    node_visitor = NodeVisitor(stats, file_path)

    assert node_visitor.stats == stats
    assert node_visitor.rel_file_path == file_path
