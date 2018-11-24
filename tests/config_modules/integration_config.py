"""
This module is used by integration tests
"""

import os

from codewatch import assertion, inference, visit

from astroid import nodes, MANAGER
from astroid.builder import AstroidBuilder


# only visit this file itself
def file_filter(file_name):
    this_file = os.path.basename(__file__)

    # make sure it's a .py file (not .pyc)
    this_file = os.path.splitext(this_file)[0] + '.py'
    return file_name == this_file


def directory_filter(_):
    return True


class A(object):
    class objects(object):
        @staticmethod
        def get():
            pass


A.objects.get()


def is_a_object_get(node):
    if not hasattr(node.func, "expr"):
        return False

    if not hasattr(node.func.expr, "expr"):
        return False

    if not node.func.expr.expr.name == 'A':
        return False

    if not node.func.expr.attrname == 'objects':
        return False

    if not node.func.attrname == 'get':
        return False

    return True


def infer_objects_get_as_a(node, context=None):
    builder = AstroidBuilder(MANAGER)
    m = builder.string_build(
        """\
class A(object):
    class objects(object):
        @staticmethod
        def get():
            pass"""
    )
    class_node = m.body[0]

    return iter((class_node.instantiate_class(),))


@visit(
    nodes.Call,
    predicate=is_a_object_get,
    inferences=[inference(nodes.Call, infer_objects_get_as_a, is_a_object_get)]
)
def call_visitor(node, stats, _rel_file_path):
    inf_types = node.inferred()
    stats.append("inferred A.objects.get()", inf_types)


def always_true_predicate(_node):
    return True


@visit(
    nodes.Call,
    inferences=[
        inference(nodes.Call, infer_objects_get_as_a, always_true_predicate),
    ],
)
def predicate_visitor_inference(_node, stats, _rel_file_path):
    stats.increment("predicate_visitor_inference")


def infer_itself(node, context=None):
    return iter((node,))


@visit(
    nodes.Call,
    inferences=[
        inference(nodes.Import, infer_itself),
        inference(nodes.ImportFrom, infer_itself),
    ],
)
def multiple_inferences(node, stats, _rel_file_path):
    import_node = node.root().body[0]
    inference_works = import_node.inferred()[0] == import_node
    stats.append('importInference', inference_works)

    import_from_node = node.root().body[1]
    inference_works = import_from_node.inferred()[0] == import_from_node
    stats.append('importFromInference', inference_works)


@assertion()
def import_inference_worked(stats):
    assert 'importInference' in stats, 'inference failed'


@assertion()
def import_from_inference_worked(stats):
    assert 'importFromInference' in stats, 'inference failed'


@visit(
    nodes.Call,
    predicate=always_true_predicate,
)
def predicate_visitor(_node, stats, _rel_file_path):
    stats.increment("predicate_visitor")


@visit(nodes.Expr)
def count_expressions(node, stats, _rel_file_path):
    stats.increment('num_expressions')
    return node


@visit(nodes.ImportFrom)
def count_imports(node, stats, _rel_file_path):
    stats.increment('num_import_from')
    return node


@assertion()
def correctly_rewritten_inference(stats):
    inference_results = stats.get('inferred A.objects.get()')
    assert len(inference_results) == 1, \
        "Too many possible inferences {i}".format(i=inference_results)
    qname = inference_results[0].qname()
    assert qname == '.A', "bad inferrence {qname}".format(qname=qname)


@assertion()
def num_import_from_more_than_zero(stats):
    err = 'num_import_from is not more than 0'
    assert stats.get('num_import_from', 0) > 0, err


@assertion()
def expressions_more_than_zero(stats):
    assert stats.get('num_expressions', 0) > 0, 'not more than zero'


@assertion(label='custom_label_always_true')
def always_true(_stats):
    assert True


@assertion(stats_namespaces=['level1'])
def always_false(_stats):
    assert False, 'should always be false'


@assertion()
def predicate_works(stats):
    assert stats.get('predicate_visitor', -1) > 0, 'predicate not working'


@assertion()
def predicate_inference_works(stats):
    assert stats.get('predicate_visitor_inference', -1) > 0, \
        'predicate not working'
