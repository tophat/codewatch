# -*- coding: utf-8 -*-

import astroid
import os
from contextlib import contextmanager

import pytest
from io import StringIO

from codewatch.run import Analyzer


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


class MockFileOpener(object):
    def __init__(self, mock_file_contents):
        self.mock_file_contents = self._as_unicode(mock_file_contents)
        self.opens = []

    def _as_unicode(self, str):
        if type(str) is bytes:
            return str.decode('utf-8')
        return str

    @contextmanager
    def open(self, *args, **kwargs):
        file_as_string_io = StringIO(self.mock_file_contents)
        self.opens.append((args, kwargs))
        yield file_as_string_io


def _test_visits_file_with_ast_tree_and_relative_path(file_contents):
    file_opener = MockFileOpener(file_contents)
    file_walker = MockFileWalker(MOCK_FILES)
    node_master = MockNodeMaster()
    analyzer = Analyzer(
        MOCK_BASE_DIRECTORY_PATH,
        file_walker,
        node_master,
        file_opener.open,
    )
    analyzer.run()

    assert len(file_opener.opens) == len(MOCK_FILES)
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


@pytest.mark.parametrize('file', [
    NORMAL_FILE,
    UTF8_FILE,
    UTF8_FILE_CODING_LINE2,
])
def test_visits_file_with_ast_tree_and_relative_path(file):
    _test_visits_file_with_ast_tree_and_relative_path(file)
