import astroid
import io
import logging
import os
import re
import sys

from codewatch.assertion import Assertion
from codewatch.file_walker import FileWalker
from codewatch.loader import ModuleLoader
from codewatch.node_visitor import NodeVisitorMaster
from codewatch.stats import Stats

logger = logging.getLogger(__name__)

NOT_DIR_ERR = (
    'codewatch_config_module should be a module name, NOT a directory'
)


class Runner(object):
    def __init__(self, base_directory, codewatch_config_module):
        self.codewatch_config_module = codewatch_config_module
        self.base_directory = base_directory

    def run(self):
        if '/' in self.codewatch_config_module:
            raise ValueError(NOT_DIR_ERR)

        try:
            sys.path.insert(0, self.base_directory)
            NodeVisitorMaster.node_visitor_registry = []
            loader = ModuleLoader(self.codewatch_config_module)
            stats = Stats()

            file_walker = FileWalker(loader, self.base_directory)
            analyzer = Analyzer(self.base_directory, file_walker)
            analyzer.run(stats)
            checker = AssertionChecker(loader, stats)
            return checker.run()
        finally:
            del sys.path[0]


class AssertionChecker(object):
    def __init__(self, loader, stats):
        self.stats = stats
        self.assertions = loader.assertions

    def run(self):
        assertion_runner = Assertion(self.stats, self.assertions)
        return assertion_runner.run()


class Analyzer(object):
    # https://www.python.org/dev/peps/pep-0263/
    CODING_REGEX = re.compile(
        r"^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)"
    )

    def __init__(
        self,
        base_directory_path,
        file_walker,
        file_opener_fn=io.open,
        parser_fn=astroid.parse,
    ):
        self.base_directory_path = base_directory_path
        self.file_walker = file_walker
        self.file_opener_fn = file_opener_fn
        self.parser_fn = parser_fn
        self.node_visitor_master_class = NodeVisitorMaster

    def _get_file_contents(self, file_name):
        with self.file_opener_fn(file_name, encoding="utf-8") as fp:
            line1, line2 = fp.readline(), fp.readline()
            file_contents = u""
            if not bool(self.CODING_REGEX.match(line1)):
                file_contents += line1
            if not bool(self.CODING_REGEX.match(line2)):
                file_contents += line2
            file_contents += fp.read()
            return file_contents

    def run(self, stats):
        for file_name in self.file_walker.walk():
            file_contents = self._get_file_contents(file_name)
            tree = self.parser_fn(file_contents, os.path.basename(file_name))
            rel_file_path = os.path.relpath(
                file_name, self.base_directory_path
            )
            self.node_visitor_master_class.visit(stats, tree, rel_file_path)

    def override_node_visitor_master(self, node_visitor_master_class):
        """Dep inj test helper to replace and reset a custom NodeVisitorMaster
        """
        node_visitor_master_class.visited = []
        self.node_visitor_master_class = node_visitor_master_class
