"""
This module is used by integration tests
"""

import os

from codewatch import (
    assertion,
    NodeVisitor,
    visit,
)


# only visit this file itself
def file_filter(file_name):
    this_file = os.path.basename(__file__)

    # make sure it's a .py file (not .pyc)
    this_file = os.path.splitext(this_file)[0] + '.py'
    return file_name == this_file


def directory_filter(_):
    return True


class MyVisitor(NodeVisitor):
    def visit_Expr(self, _node):
        self.stats.increment('num_expressions')


@visit('importFrom')
def count_imports(self, _node):
    self.stats.increment('num_import_from')


@assertion()
def num_import_from_more_than_zero(stats):
    err = 'num_import_from is not more than 0'
    return stats.get('num_import_from', 0) > 0, err


@assertion()
def expressions_more_than_zero(stats):
    return stats.get('num_expressions', 0) > 0, 'not more than zero'


@assertion(label='custom_label_always_true')
def always_true(_stats):
    return True, None


@assertion(stats_namespaces=['level1'])
def always_false(_stats):
    return False, 'should always be false'
