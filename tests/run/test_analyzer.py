# -*- coding: utf-8 -*-

import astroid
import os
from contextlib import contextmanager

from codewatch.run import Analyzer

try:
    # python 2
    from unittest import mock
except ImportError:
    # python 3
    import mock
open_path = 'io.open'


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


def _as_unicode(str):
    if type(str) is bytes:
        return str.decode('utf-8')
    return str


@contextmanager
def patch_open(file_contents, num_files):
    open_mock = mock.MagicMock()
    split = _as_unicode(file_contents).split('\n')
    # this mock will only work if there's 3 or more lines
    assert len(split) >= 3

    line1, line2, rest = split[0], split[1], split[2:]
    read_line_values = [line1 + '\n', line2 + '\n'] * num_files

    open_mock.readline.side_effect = read_line_values
    open_mock.read.return_value = '\n'.join(rest)
    with mock.patch(open_path, return_value=open_mock) as m:
        yield m


def _test_visits_file_with_ast_tree_and_relative_path(file_contents):
    with patch_open(file_contents, len(MOCK_FILES)) as m:
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
            assert isinstance(tree, astroid.Module)
            expected_file_path = RELATIVE_MOCK_FILE_PATHS[i]
            assert file_path == expected_file_path


NORMAL_FILE = (
    'a = 3\n'
    'b = 3\n'
)
UTF8_FILE = (
    '# -*- coding: utf-8 -*-\n'
    'a = "你好，世界"\n'
)
UTF8_FILE_CODING_LINE2 = (
    '\n'
    '# -*- coding: utf-8 -*-\n'
    'a = "你好，世界"\n'
)


def test_visits_file_with_ast_tree_and_relative_path():
    _test_visits_file_with_ast_tree_and_relative_path(NORMAL_FILE)


def test_visits_file_with_ast_tree_and_relative_path_utf8():
    _test_visits_file_with_ast_tree_and_relative_path(UTF8_FILE)


def test_visits_file_with_ast_tree_and_relative_path_utf8_line2():
    _test_visits_file_with_ast_tree_and_relative_path(UTF8_FILE_CODING_LINE2)
