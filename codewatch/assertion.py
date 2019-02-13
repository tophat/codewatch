from functools import wraps
from sys import exc_info
from traceback import extract_tb


def _get_assertion_failure_message(assertion_failure):
    """
    if there's an assertion error message return that
    otherwise, return the code line the assertion is called from
    """
    if assertion_failure.args:
        return assertion_failure.args[0]
    # extract_tb returns a StackSummary, which wraps a list of FrameSummary
    tb_info = extract_tb(exc_info()[2])
    # FrameSummary contains:
    # (self.filename, self.lineno, self.name, self.line)
    # Get the last FrameSummary then get the line's text
    return tb_info[-1][3]


class Assertion(object):
    def __init__(self, stats, assertion_fns):
        self.stats = stats
        self.assertion_fns = assertion_fns

    @staticmethod
    def load_assertion_fns(module):
        assertions = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if not callable(attr):
                continue
            if not hasattr(attr, '_wrapped_assertion_label'):
                continue
            assertions.append(attr)
        return assertions

    def run(self):
        successes = []
        failures = {}
        errors = {}

        for assertion_fn in self.assertion_fns:
            assertion_label = assertion_fn._wrapped_assertion_label
            try:
                assertion_fn(self.stats)
            except AssertionError as assertion_failure:
                failures[assertion_label] = _get_assertion_failure_message(
                    assertion_failure,
                )
            except Exception as error:
                errors[assertion_label] = error
            else:
                successes.append(assertion_label)
        return successes, failures, errors


def _with_stats_namespace(*namespaces):
    def decorator(fn):
        @wraps(fn)
        def wrapper(stats, *args, **kwargs):
            _stats = stats
            for namespace in namespaces:
                _stats = _stats.namespaced(namespace)
            return fn(_stats, *args, **kwargs)
        return wrapper
    return decorator


def assertion(label=None, stats_namespaces=None):
    def decorator(fn):
        _label = label
        if _label is None:
            _label = fn.__name__
        _stats_namespaces = stats_namespaces
        if _stats_namespaces is None:
            _stats_namespaces = []

        @_with_stats_namespace(*_stats_namespaces)
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapper._wrapped_assertion_label = _label
        return wrapper
    return decorator
