# -*- coding: utf-8 -*-

from astroid import nodes
from codewatch import (
    assertion,
    visit,
)

import os


hello_world = '你好，世界'


def file_filter(file_name):
    this_file = os.path.basename(__file__)

    # make sure it's a .py file (not .pyc)
    this_file = os.path.splitext(this_file)[0] + '.py'
    return file_name == this_file


def directory_filter(_dir_name):
    return True


@visit(nodes.Expr)
def count_expressions(node, stats, _rel_file_path):
    stats.increment(hello_world)
    return node


@assertion()
def unicode_works(stats):
    assert stats.get(hello_world, 0) > 0, 'unicode not working'
