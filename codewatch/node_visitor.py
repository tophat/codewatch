import ast


class NodeVisitor(ast.NodeVisitor):
    def __init__(self, stats, rel_file_path):
        self.stats = stats
        self.rel_file_path = rel_file_path
