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
    'annotate',
    'bulk_create',
    'distinct',
    'exclude',
    'filter',
    'order_by',
    'prefetch_related',
    'select_related',
    'using',
)

DJANGO_MANAGER_METHODS = (
    'first',
    'last',
    'get',
    'create',
    'latest',
    'get_or_create',
    'update_or_create',
) + DJANGO_MANAGER_METHODS_LIST


def get_inference_for_model(model_qname):
    def _did_we_infer(node):
        """
        Checks to see if we inferred this node as part of _inf_fn

        Only the DJANGO_MANAGER_METHODS_LIST methods are chainable
        so we only need to detect the inferences we made on those
        """
        try:
            inferred = next(node.infer())
        except InferenceError:
            return False, None
        if not isinstance(inferred, nodes.List):
            return False, None
        if inferred.ctx != LoadContext:
            return False, None
        if len(inferred.elts) != 1:
            return False, None
        if inferred.elts[0].pytype() != model_qname:
            return False, None
        return True, inferred.elts[0]

    def _inf_pred(node):
        """
        Returns true if it's either:
        1) A normal Django Manager call, eg: DjangoUserModel.objects.get()
        2) A Django Manager method call on a node we previously inferred
            eg: all_users.first()
        """
        if (
            not hasattr(node.func, 'attrname')
            or node.func.attrname not in DJANGO_MANAGER_METHODS
        ):
            return False

        if not hasattr(node.func, 'expr'):
            return

        if (
            not hasattr(node.func.expr, 'attrname')
            or node.func.expr.attrname != 'objects'
        ):
            # Check for case 2)
            did_we_infer, klass_obj = _did_we_infer(node.func.expr)
            if did_we_infer:
                node._codewatch_inferred_model_klass_obj = klass_obj
            return did_we_infer
        if not hasattr(node.func.expr, 'expr'):
            return False

        klass_name_node = node.func.expr.expr
        try:
            inferred = klass_name_node.inferred()
        except InferenceError:
            return False
        return inferred[0].qname() == model_qname

    def _inf_fn(node, context=None):
        if hasattr(node, '_codewatch_inferred_model_klass_obj'):
            # For the case where we already inferred the manager call
            # We just need to infer the new call
            # eg:
            #   users = DjangoUser.objects.all()
            #   users.first()
            #
            # users.first() is the node we are inferring
            #
            # Astroid will take care of calling `infer` on `users`
            # Here we detected that `users` is an inference we returned
            klass_obj = node._codewatch_inferred_model_klass_obj
        else:
            # Otherwise, it's a bare manager call, eg: DjangoUser.objects.all()
            klass_def = node.func.expr.expr.inferred()[0]
            klass_obj = klass_def.instantiate_class()

        if node.func.attrname in DJANGO_MANAGER_METHODS_LIST:
            # we infer a `List` node with a single `klass_obj` element
            klass_obj_list = nodes.List(ctx=LoadContext)
            klass_obj_list.elts = [klass_obj]
            return iter((klass_obj_list,))
        # otherwise, just infer the `klass_obj`
        return iter((klass_obj,))

    return inference(nodes.Call, _inf_fn, _inf_pred)
