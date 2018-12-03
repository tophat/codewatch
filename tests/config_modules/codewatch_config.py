from codewatch.assertion import assertion


@assertion()
def error_assertion(_stats):
    # throw an exception
    KeyError(0)
