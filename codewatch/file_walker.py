import os


class FileWalker(object):
    def __init__(self, loader, base_directory_path):
        self.base_directory_path = base_directory_path
        self.directory_visitor, self.file_visitor = loader.load_file_filters()

    def walk(self):
        for path, directories, files in os.walk(self.base_directory_path):
            rel_path = os.path.relpath(path, self.base_directory_path)
            path_basename = os.path.basename(path)
            if (
                rel_path != '.'
                and not self.directory_visitor(path_basename)
            ):
                continue

            for file in files:
                if not self.file_visitor(file):
                    continue
                yield os.path.join(path, file)