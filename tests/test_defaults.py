import pytest

from codewatch.defaults import (
    create_directory_filter,
    create_file_filter,
)


@pytest.mark.parametrize('dir_name,expected_output', [
    ('migrations', False),
    ('normal_dir', True),
    ('test_dir', False),
    ('another_test', False),
    ('another_normal', True),
])
def test_default_directory_filter(dir_name, expected_output):
    dir_filter = create_directory_filter()
    assert dir_filter(dir_name) == expected_output


@pytest.mark.parametrize('file_name,expected_output', [
    ('normal_python_file.py', True),
    ('non_python_file.txt', False),
    ('test_py_file.py', False),
    ('a_pyc_file.pyc', False),
])
def test_default_file_filter(file_name, expected_output):
    dir_filter = create_file_filter()
    assert dir_filter(file_name) == expected_output
