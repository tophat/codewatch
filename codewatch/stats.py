class Stats(object):
    def __init__(self, base_stats=None, namespace=None):
        if base_stats is None:
            base_stats = {}
        if namespace is None:
            stats = base_stats
        else:
            if namespace not in base_stats:
                base_stats[namespace] = {}
            stats = base_stats[namespace]

        self.base_stats = base_stats
        self.stats = stats

    def __getattr__(self, item):
        return self.stats.__getattribute__(item)

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
