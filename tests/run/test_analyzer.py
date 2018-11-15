import ast
import os
from contextlib import contextmanager

from codewatch.run import Analyzer

try:
    # python 2
    from unittest import mock
    open_path = 'builtins.open'
except ImportError:
    # python 3
    import mock
    open_path = '__builtin__.open'


MOCK_BASE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
RELATIVE_MOCK_FILE_PATHS = (
    'mockdir/mockfile1',
    'mockdir/mockfile2',
)
MOCK_FILES = [
    os.path.join(MOCK_BASE_DIRECTORY_PATH, RELATIVE_MOCK_FILE_PATHS[0]),
    os.path.join(MOCK_BASE_DIRECTORY_PATH, RELATIVE_MOCK_FILE_PATHS[1]),
]


class MockFileWalker(object):
    def __init__(self, mock_files):
        self.mock_files = mock_files

    def walk(self):
        return self.mock_files


class MockNodeMaster(object):
    def __init__(self):
        self.visited = []

    def visit(self, tree, file_path):
        self.visited.append((tree, file_path))


@contextmanager
def patch_open(file_contents):
    open_mock = mock.MagicMock()
    open_mock.read.return_value = file_contents

    with mock.patch(open_path, return_value=open_mock) as m:
        yield m


def test_visits_file_with_ast_tree_and_relative_path():
    with patch_open('') as m:
        file_walker = MockFileWalker(MOCK_FILES)
        node_master = MockNodeMaster()
        analyzer = Analyzer(
            MOCK_BASE_DIRECTORY_PATH,
            file_walker,
            node_master,
        )
        analyzer.run()

        assert m.call_count == len(MOCK_FILES)
        assert len(node_master.visited) == len(MOCK_FILES)

        for i, (tree, file_path) in enumerate(node_master.visited):
            assert isinstance(tree, ast.Module)
            expected_file_path = RELATIVE_MOCK_FILE_PATHS[i]
            assert file_path == expected_file_path
