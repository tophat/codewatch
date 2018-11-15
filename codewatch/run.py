import ast
import logging
import os
import sys

from codewatch.assertion import Assertion
from codewatch.file_walker import FileWalker
from codewatch.loader import ModuleLoader
from codewatch.stats import Stats

logger = logging.getLogger(__name__)


class Runner(object):
    def __init__(self, base_directory, codewatch_config_module):
        self.codewatch_config_module = codewatch_config_module
        self.base_directory = base_directory

    def run(self):
        try:
            sys.path.insert(0, self.base_directory)
            loader = ModuleLoader(self.codewatch_config_module)
            stats = Stats()

            file_walker = FileWalker(loader, self.base_directory)
            node_master = NodeVisitorMaster(loader, stats)
            analyzer = Analyzer(self.base_directory, file_walker, node_master)
            analyzer.run()
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
    def __init__(
        self,
        base_directory_path,
        file_walker,
        node_visitor_master,
    ):
        self.base_directory_path = base_directory_path
        self.file_walker = file_walker
        self.node_visitor_master = node_visitor_master

    def run(self):
        for file in self.file_walker.walk():
            file_contents = open(file).read()
            tree = ast.parse(file_contents, os.path.basename(file))
            rel_file_path = os.path.relpath(file, self.base_directory_path)
            self.node_visitor_master.visit(tree, rel_file_path)


class NodeVisitorMaster(object):
    def __init__(self, loader, stats):
        self.stats = stats
        self.node_visitors = loader.visitors

    def _initialize_node_visitors(self, rel_file_path):
        return [
            node_visitor(self.stats, rel_file_path)
            for node_visitor in self.node_visitors
        ]

    def visit(self, node, rel_file_path):
        node_visitors_initialized = self._initialize_node_visitors(
            rel_file_path,
        )

        for node_visitor_initialized in node_visitors_initialized:
            node_visitor_initialized.visit(node)
