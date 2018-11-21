import pytest

from codewatch.defaults import (
    create_directory_filter,
    create_file_filter,
)


@pytest.mark.parametrize('dir_name,directory_filters,expected_output', [
    ('migrations', None, False),
    ('migrations', [], True),

    ('normal_dir', None, True),
    ('another_normal', None, True),

    ('test_dir', None, False),
    ('test_dir', [], True),
    ('another_test', None, False),
])
def test_create_directory_filter(
    dir_name,
    directory_filters,
    expected_output,
):
    dir_filter = create_directory_filter(directory_filters)
    assert dir_filter(dir_name) == expected_output


@pytest.mark.parametrize('file_name,file_filters,expected_output', [
    ('normal_python_file.py', None, True),
    ('non_python_file.txt', None, False),
    ('non_python_file.txt', [], True),
    ('a_pyc_file.pyc', None, False),
    ('test_py_file.py', None, False),
    ('test_py_file.py', [], True),
])
def test_create_file_filter(file_name, file_filters, expected_output):
    file_filter = create_file_filter(file_filters)
    assert file_filter(file_name) == expected_output
