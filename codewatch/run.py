import ast
import logging
import os
from datetime import datetime

from codewatch.file_walker import FileWalker
from codewatch.stats import Stats

logger = logging.getLogger(__name__)


class AssertionChecker(object):
    def __init__(self, loader, stats):
        self.stats = stats
        self.assertions = loader.load_assertions()

    def run(self):
        initialized_assertions = [
            assertion(self.stats) for assertion in self.assertions
        ]
        successes = []
        failures = {}

        for assertion_obj in initialized_assertions:
            assertion_obj.run(successes, failures)
        return successes, failures


class Analyzer(object):
    def __init__(self, loader, base_directory_path):
        self.stats = Stats()
        self.meta_stats = self.stats.namespaced('META').namespaced('ANALYZER')
        self.base_directory_path = base_directory_path
        self.file_walker = FileWalker(
            loader,
            base_directory_path,
        )
        self.node_visitor_master = NodeVisitorMaster(
            loader,
            self.stats,
        )

    def _log_meta_stats(self):
        logger.debug('time taken: {}'.format(self.meta_stats.get('runtime')))
        logger.debug('num files walked: {}'.format(
            self.meta_stats.get('visited_files'),
        ))

    def run(self):
        start = datetime.now()
        for file in self.file_walker.walk():
            file_contents = open(file).read()
            tree = ast.parse(file_contents, os.path.basename(file))
            rel_file_path = os.path.relpath(file, self.base_directory_path)
            self.node_visitor_master.visit(tree, rel_file_path)
            self.meta_stats.increment('visited_files')
        end = datetime.now()

        self.meta_stats.append('runtime', end - start)
        self._log_meta_stats()
        return self.stats


class NodeVisitorMaster(object):
    def __init__(self, loader, stats):
        self.stats = stats
        self.node_visitors = loader.load_node_visitors()

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
