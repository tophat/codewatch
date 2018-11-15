"""
This module is used by integration tests
"""

import os

from codewatch import (
    Assertion,
    NodeVisitor,
)


# only visit this file itself
def file_filter(file_name):
    this_file = os.path.basename(__file__)
    return file_name == this_file


def directory_filter(_):
    return True


class MyVisitor(NodeVisitor):
    def visit_Expr(self, node):
        self.stats.increment('num_expressions')


class MyAssertion(Assertion):
    def assert_expressions_more_than_zero(self):
        return self.stats.get('num_expressions') > 0, 'not more than zero'

    def assert_always_true(self):
        return True, None

    def assert_always_false(self):
        return False, 'should always be false'
