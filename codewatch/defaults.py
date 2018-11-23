import re

PYTHON_FILE_REGEX = re.compile(r'.*.py$')
TEST_FILE_REGEX = re.compile(r'.*test.*')
MIGRATION_DIRECTORY_REGEX = re.compile(r'.*migrations.*')


def is_python_file_filter(file_name):
    return bool(PYTHON_FILE_REGEX.match(file_name))


def is_not_test_file_filter(file_name):
    return not bool(TEST_FILE_REGEX.match(file_name))


def is_not_test_directory_filter(dir_name):
    return not bool(TEST_FILE_REGEX.match(dir_name))


def is_not_migration_directory_filter(dir_name):
    return not bool(MIGRATION_DIRECTORY_REGEX.match(dir_name))


DEFAULT_DIRECTORY_FILTERS = [
    is_not_test_directory_filter,
    is_not_migration_directory_filter,
]

DEFAULT_FILE_FILTERS = [
    is_python_file_filter,
    is_not_test_file_filter,
]


def create_directory_filter(
    directory_filters=None,
):
    if directory_filters is None:
        directory_filters = DEFAULT_DIRECTORY_FILTERS

    def directory_filter(dir_name):
        should_visit_dir = True
        for filter_fn in directory_filters:
            should_visit_dir &= filter_fn(dir_name)
        return should_visit_dir
    return directory_filter


def create_file_filter(
    file_filters=None,
):
    if file_filters is None:
        file_filters = DEFAULT_FILE_FILTERS

    def file_filter(file_name):
        should_visit_file = True
        for filter_fn in file_filters:
            should_visit_file &= filter_fn(file_name)
        return should_visit_file
    return file_filter
