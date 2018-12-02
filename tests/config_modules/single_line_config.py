# -*- coding: utf-8 -*-

from astroid import nodes
from codewatch import (
    assertion,
    visit,
)


def file_filter(file_name):
    return file_name == 'single_print.py'


@visit(nodes.Call)
def count_prints(node, stats, _rel_file_path):
    if node.func.name == 'print':
        stats.increment('print')


@visit(nodes.Print)
def count_prints(node, stats, _rel_file_path):
    stats.increment('print')


@assertion()
def single_file_works(stats):
    assert stats.get('print', 0) == 1, 'single file not working'
