from codewatch import Stats


def test_can_insert_and_retrieve_value():
    stats = Stats()
    stats.append('abc', 123)
    assert stats.get('abc') == 123
