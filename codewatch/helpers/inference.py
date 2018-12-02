from astroid import (
    Load as LoadContext,
    nodes,
    InferenceError,
)

from codewatch.node_visitor import Inference


def inference(node, fn, predicate=None):
    return Inference(node, fn, predicate)


DJANGO_MANAGER_METHODS_LIST = (
    'all',
    'bulk_create',
    'filter',
    'order_by',
)

DJANGO_MANAGER_METHODS = (
    'get',
    'create',
    'latest',
    'get_or_create',
    'update_or_create',
) + DJANGO_MANAGER_METHODS_LIST


def get_inference_for_model(model_qname):
    def _inf_pred(node):
        if (
            not hasattr(node.func, 'attrname')
            or node.func.attrname not in DJANGO_MANAGER_METHODS
        ):
            return False
        if (
            not hasattr(node.func, 'expr')
            or not hasattr(node.func.expr, 'attrname')
            or node.func.expr.attrname != 'objects'
        ):
            return False
        if not hasattr(node.func.expr, 'expr'):
            return False

        klass_name_node = node.func.expr.expr
        try:
            inferred = klass_name_node.inferred()
        except InferenceError:
            return False
        return inferred[0].qname() == model_qname

    def _inf_fn(node, context=None):
        klass_def = node.func.expr.expr.inferred()[0]
        klass_obj = klass_def.instantiate_class()

        if node.func.attrname in DJANGO_MANAGER_METHODS_LIST:
            klass_obj_list = nodes.List(ctx=LoadContext)
            klass_obj_list.elts = [klass_obj]
            return iter((klass_obj_list,))
        return iter((klass_obj,))

    return inference(nodes.Call, _inf_fn, _inf_pred)
