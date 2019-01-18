from os import walk as os_walk
from os.path import join


class FileWalker(object):
    def __init__(self, loader, base_directory_path, walk_fn=None):
        self.base_directory_path = base_directory_path
        self.directory_filter, self.file_filter = loader.filters

        if walk_fn is None:
            walk_fn = os_walk
        self.walk_fn = walk_fn

    def walk(self):
        for path, directories, files in self.walk_fn(self.base_directory_path):
            directories[:] = [
                d for d in directories
                if self.directory_filter(join(path, d))
            ]

            for file in files:
                if not self.file_filter(file):
                    continue
                yield join(path, file)
