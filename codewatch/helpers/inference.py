from astroid import (
    InferenceError,
    nodes,
)

from codewatch.node_visitor import Inference


def inference(node, fn, predicate=None):
    return Inference(node, fn, predicate)


class DjangoInferenceHelpers(object):
    MANAGER_METHODS = (
        'get',
        'create',
        'get_or_create',
        'update_or_create',
    )

    @classmethod
    def get_inference_for_model(cls, model_qname):
        def _inf_pred(node):
            if (
                not hasattr(node.func, 'attrname')
                or node.func.attrname not in cls.MANAGER_METHODS
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

        def _inf(node, context=None):
            klass_def = node.func.expr.expr.inferred()[0]
            return iter((klass_def.instantiate_class(),))

        return _inf, _inf_pred
