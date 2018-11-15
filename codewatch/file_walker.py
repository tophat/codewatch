from os import walk as os_walk
from os.path import (
    basename,
    join,
    relpath,
)


class FileWalker(object):
    def __init__(self, loader, base_directory_path, walk_fn=None):
        self.base_directory_path = base_directory_path
        self.directory_filter, self.file_filter = loader.filters

        if walk_fn is None:
            walk_fn = os_walk
        self.walk_fn = walk_fn

    def walk(self):
        for path, directories, files in self.walk_fn(self.base_directory_path):
            rel_path = relpath(path, self.base_directory_path)
            path_basename = basename(path)
            if rel_path != '.' and not self.directory_filter(path_basename):
                continue

            for file in files:
                if not self.file_filter(file):
                    continue
                yield join(path, file)
