import pytest

from codewatch.defaults import (
    create_directory_filter,
    create_file_filter,
)


@pytest.mark.parametrize('dir_name,kwargs,expected_output', [
    ('migrations', {}, False),
    ('migrations', {'exclude_migration_dirs': False}, True),

    ('normal_dir', {}, True),
    ('another_normal', {}, True),

    ('test_dir', {}, False),
    ('test_dir', {'exclude_test_dirs': False}, True),
    ('another_test', {}, False),
])
def test_create_directory_filter(dir_name, kwargs, expected_output):
    dir_filter = create_directory_filter(**kwargs)
    assert dir_filter(dir_name) == expected_output


@pytest.mark.parametrize('file_name,kwargs,expected_output', [
    ('normal_python_file.py', {}, True),
    ('non_python_file.txt', {}, False),
    ('non_python_file.txt', {'only_include_py_files': False}, True),
    ('a_pyc_file.pyc', {}, False),
    ('test_py_file.py', {}, False),
    ('test_py_file.py', {'exclude_test_files': False}, True),
])
def test_default_file_filter(file_name, kwargs, expected_output):
    file_filter = create_file_filter(**kwargs)
    assert file_filter(file_name) == expected_output
