import pytest
from astroid import (
    nodes,
    parse,
)
from codewatch.predicates import (
    CallNodePredicates,
)


NESTED_FN_CALL_CODE = """\
class A(object):
    @staticmethod
    def a():
        return A
    @staticmethod
    def b():
        return A
    @staticmethod
    def c():
        return A
    @staticmethod
    def d():
        return A

    @property
    def p1(self):
        return A
    @property
    def p2(self):
        return A
    @property
    def p3(self):
        return A

A.a().b().c().d()
A.p1.p2.p3.d()
"""

QNAME_INFERENCE_CODE = """\
class Grade(object):
    class nested(object):
        pass
    def get_nested(self):
        return Grade.nested()

grade = Grade().get_nested()
"""


QNAME_UNINFERABLE_CODE = """\
from my_models import Grade
Grade()
"""


@pytest.mark.parametrize('code,method_name,expected_value', [
    (NESTED_FN_CALL_CODE, 'A.a.b.c.d', True),
    (NESTED_FN_CALL_CODE, 'A', False),
    (NESTED_FN_CALL_CODE, 'a.b.c.d', False),
    (NESTED_FN_CALL_CODE, 'd', False),
    (NESTED_FN_CALL_CODE, 'A.a.x.c.d', False),
])
def test_does_node_call_method_as_fn_calls(code, method_name, expected_value):
    call_node = parse(code).body[1].value
    assert type(call_node) == nodes.Call

    ret = CallNodePredicates.has_expected_chain_name(
        call_node,
        method_name,
    )
    assert ret == expected_value


@pytest.mark.parametrize('code,method_name,expected_value', [
    (NESTED_FN_CALL_CODE, 'A.p1.p2.p3.d', True),
    (NESTED_FN_CALL_CODE, 'A', False),
    (NESTED_FN_CALL_CODE, 'p1.p2.p3.d', False),
    (NESTED_FN_CALL_CODE, 'd', False),
])
def test_does_node_call_method_as_attr(code, method_name, expected_value):
    call_node = parse(code).body[2].value
    assert type(call_node) == nodes.Call

    ret = CallNodePredicates.has_expected_chain_name(
        call_node,
        method_name,
    )
    assert ret == expected_value


@pytest.mark.parametrize('code,qname,expected_value', [
    (QNAME_INFERENCE_CODE, 'my_test_module.Grade.nested', True),
    (QNAME_INFERENCE_CODE, 'nested', False),
    (QNAME_INFERENCE_CODE, 'Grade.nested', False),
    (QNAME_INFERENCE_CODE, 'object', False),
])
def test_is_node_qname_inferred(code, qname, expected_value):
    node = parse(code, 'my_test_module').body[1].value
    assert type(node) == nodes.Call
    ret = CallNodePredicates.has_expected_qname(node, qname)
    assert ret == expected_value


@pytest.mark.parametrize('code,qname,expected_value', [
    (QNAME_UNINFERABLE_CODE, 'my_models.Grade', False),
])
def test_is_node_qname_inferred_uninferable(code, qname, expected_value):
    import_from_node = parse(code, 'my_test_module').body[0]
    assert type(import_from_node) == nodes.ImportFrom

    ret = CallNodePredicates.has_expected_qname(
        import_from_node,
        qname,
    )
    assert ret == expected_value
