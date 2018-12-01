# -*- coding: utf-8 -*-

import os
from contextlib import contextmanager
from io import StringIO

import astroid
import pytest
from codewatch.run import Analyzer
from codewatch.stats import Stats


MOCK_BASE_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
MOCK_FILE_NAMES = ("mockfile1.py", "mockfile2.py")
RELATIVE_MOCK_FILE_PATHS = (
    os.path.normcase("mockdir/" + MOCK_FILE_NAMES[0]),
    os.path.normcase("mockdir/" + MOCK_FILE_NAMES[1]),
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
    visited = []

    @classmethod
    def visit(cls, stats, tree, file_path):
        cls.visited.append((tree, file_path))


def _as_unicode(str):
    if type(str) is bytes:
        return str.decode("utf-8")
    return str


class MockFileOpener(object):
    def __init__(self, mock_file_contents):
        self.mock_file_contents = _as_unicode(mock_file_contents)
        self.opens = []

    @contextmanager
    def open(self, *args, **kwargs):
        file_as_string_io = StringIO(self.mock_file_contents)
        self.opens.append((args, kwargs))
        yield file_as_string_io


class MockParser(object):
    def __init__(self, mock_tree):
        self.mock_tree = mock_tree
        self.parses = []

    def parse(self, *args, **kwargs):
        self.parses.append((args, kwargs))
        return self.mock_tree


def _test_visits_file_with_ast_tree_and_relative_path(
    mock_file_contents, expected_file_contents_for_parsing
):
    mock_tree = astroid.Module(doc="", name="mock_module")
    file_opener = MockFileOpener(mock_file_contents)
    file_walker = MockFileWalker(MOCK_FILES)
    parser = MockParser(mock_tree)
    analyzer = Analyzer(
        MOCK_BASE_DIRECTORY_PATH, file_walker, file_opener.open, parser.parse
    )
    analyzer.override_node_visitor_master(MockNodeMaster)
    analyzer.run(Stats())

    assert len(file_opener.opens) == len(MOCK_FILES)
    assert len(MockNodeMaster.visited) == len(MOCK_FILES)
    assert len(parser.parses) == len(MOCK_FILES)

    for i, (tree, file_path) in enumerate(MockNodeMaster.visited):
        assert tree == mock_tree
        expected_file_path = RELATIVE_MOCK_FILE_PATHS[i]
        assert file_path == expected_file_path

    for i, (args, _) in enumerate(parser.parses):
        file_contents_received_for_parsing, file_name = args
        assert file_contents_received_for_parsing == _as_unicode(
            expected_file_contents_for_parsing
        )
        assert file_name == MOCK_FILE_NAMES[i]


NORMAL_FILE = (
    'a = 3\n'
    'b = 3\n'
)
EXPECTED_NORMAL_FILE_TO_PARSE = NORMAL_FILE


UTF8_FILE = (
    '# -*- coding: utf-8 -*-\n'
    'a = "你好，世界"\n'
)
EXPECTED_UTF8_FILE_TO_PARSE = (
    'a = "你好，世界"\n'
)


UTF8_FILE_CODING_LINE2 = (
    '\n'
    '# -*- coding: utf-8 -*-\n'
    'a = "你好，世界"\n'
)
EXPECTED_UTF8_FILE_CODING_LINE2_TO_PARSE = (
    '\n'
    'a = "你好，世界"\n'
)


@pytest.mark.parametrize(
    "file,expected_file_contents_for_parsing",
    [
        (NORMAL_FILE, EXPECTED_NORMAL_FILE_TO_PARSE),
        (UTF8_FILE, EXPECTED_UTF8_FILE_TO_PARSE),
        (UTF8_FILE_CODING_LINE2, EXPECTED_UTF8_FILE_CODING_LINE2_TO_PARSE),
    ],
)
def test_visits_file_with_ast_tree_and_relative_path(
    file, expected_file_contents_for_parsing
):
    _test_visits_file_with_ast_tree_and_relative_path(
        file, expected_file_contents_for_parsing
    )
