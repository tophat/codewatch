class Stats(object):
    def __init__(self, stats=None, namespace=None):
        if stats is None:
            stats = {}

        if namespace is not None:
            if namespace not in stats:
                stats[namespace] = {}
            stats = stats[namespace]
        self.stats = stats

    def namespaced(self, namespace):
        return Stats(self.stats, namespace)

    def append_list(self, key, val):
        if key not in self.stats:
            self.stats[key] = []
        self.stats[key].append(val)

    def increment(self, key):
        if key not in self.stats:
            self.stats[key] = 0
        self.stats[key] += 1

    def append(self, key, val):
        self.stats[key] = val

    def __str__(self):
        return self.stats.__str__()

    def __repr__(self):
        return self.stats.__repr__()

    def __getattr__(self, item):
        return self.stats.__getattribute__(item)
