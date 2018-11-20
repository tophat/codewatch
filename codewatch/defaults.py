import re

PYTHON_FILE_REGEX = re.compile(r'.*.py$')
TEST_FILE_REGEX = re.compile(r'.*test.*')
MIGRATION_DIRECTORY_REGEX = re.compile(r'.*migrations.*')


def create_directory_filter(
    exclude_test_dirs=True,
    exclude_migration_dirs=True,
):
    def directory_filter(dir_name):
        should_visit_dir = True

        if exclude_test_dirs:
            should_visit_dir &= not bool(re.match(TEST_FILE_REGEX, dir_name))
        if exclude_migration_dirs:
            should_visit_dir &= not bool(
                re.match(MIGRATION_DIRECTORY_REGEX, dir_name),
            )
        return should_visit_dir
    return directory_filter


def create_file_filter(
    exclude_test_files=True,
    only_include_py_files=True,
):
    def file_filter(file_name):
        should_visit_file = True

        if exclude_test_files:
            should_visit_file &= not bool(re.match(TEST_FILE_REGEX, file_name))
        if only_include_py_files:
            should_visit_file &= bool(re.match(PYTHON_FILE_REGEX, file_name))
        return should_visit_file
    return file_filter
