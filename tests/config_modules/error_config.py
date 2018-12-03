from codewatch.assertion import assertion


def file_filter(_file_name):
    return False


@assertion()
def error_assertion(_stats):
    # throw an exception
    raise KeyError(0)
