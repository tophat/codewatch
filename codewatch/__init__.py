from codewatch.assertion import (
    Assertion,
    with_stats_namespace,
)
from codewatch.loader import ModuleLoader
from codewatch.run import (
    Analyzer,
    AssertionChecker,
)
from codewatch.node_visitor import NodeVisitor
from codewatch.file_walker import FileWalker
from codewatch.stats import Stats

def hello_world():
    print('hello world')
    return True
