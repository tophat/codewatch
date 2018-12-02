from os.path import (normcase, join)
from codewatch.file_walker import FileWalker


MOCK_PATHS = [
    ('.', ['dir1', 'dir2'], ['file1', 'file2', 'file3']),
    (normcase('./dir1'), [], ['dir1_file1', 'dir1_file2']),
    (normcase('./dir2'), ['dir2_subdir'], ['dir2_file1']),
    (normcase('./dir2/dir2_subdir'), [], ['subdir_file1']),
]

MOCK_START_PATH = normcase('/home/mock')


def _expected_files_from_dir(dir_index):
    path = MOCK_PATHS[dir_index][0]
    files = MOCK_PATHS[dir_index][2]
    return [join(path, file) for file in files]


def create_mock_os_walk(mock_path):
    def _os_walk(path):
        assert path == mock_path
        return MOCK_PATHS
    return _os_walk


def _walk(directory_filter, file_filter):
    class MockLoader(object):
        def __init__(self, filters):
            self.filters = filters

    loader = MockLoader(filters=[directory_filter, file_filter])
    walk_fn = create_mock_os_walk(MOCK_START_PATH)
    walker = FileWalker(loader, MOCK_START_PATH, walk_fn=walk_fn)
    return [f for f in walker.walk()]


def test_it_can_walk_all_files():
    def directory_filter(_path):
        return True

    def file_filter(_path):
        return True

    expected_files_walked = (
        _expected_files_from_dir(0) +
        _expected_files_from_dir(1) +
        _expected_files_from_dir(2) +
        _expected_files_from_dir(3)
    )
    assert _walk(directory_filter, file_filter) == expected_files_walked


def test_it_filters_on_directories():
    def directory_filter(path):
        return 'dir2' not in path

    def file_filter(_path):
        return True

    expected_files_walked = (
        _expected_files_from_dir(0) +
        _expected_files_from_dir(1)
    )
    assert _walk(directory_filter, file_filter) == expected_files_walked


def test_it_filters_on_files():
    def directory_filter(_path):
        return True

    def file_filter(path):
        return 'subdir' not in path

    expected_files_walked = (
        _expected_files_from_dir(0) +
        _expected_files_from_dir(1) +
        _expected_files_from_dir(2)
    )
    assert _walk(directory_filter, file_filter) == expected_files_walked
