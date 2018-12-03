from codewatch.assertion import assertion


@assertion()
def first_assertion(_stats):
    # throw an exception
    KeyError(0)