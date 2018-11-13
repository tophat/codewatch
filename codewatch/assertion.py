from functools import wraps


class Assertion(object):
    def __init__(self, stats):
        self.base_stats = stats

    def run(self, successes, failures):
        for attr_name in dir(self):
            if 'assert_' not in attr_name:
                continue
            assertion_fn = getattr(self, attr_name)
            if not callable(assertion_fn):
                continue

            self.stats = self.base_stats
            success, err = assertion_fn()
            assertion_label = '{}.{}'.format(
                self.__class__.__name__,
                assertion_fn.__name__,
            )
            if success:
                successes.append(assertion_label)
            else:
                failures[assertion_label] = err


def with_stats_namespace(*namespaces):
    def decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            _stats = self.base_stats
            for namespace in namespaces:
                _stats = _stats.namespaced(namespace)
            self.stats = _stats
            return fn(self, *args, **kwargs)
        return wrapper
    return decorator
