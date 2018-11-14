from subprocess import call


def directory_filter(dir_name):
    return dir_name == 'codewatch'


def file_filter(file_name):
    return file_name.endswith('.py')


def test_codewatch_returns_success():
    ret = call(['codewatch', __name__])
    assert ret == 0
