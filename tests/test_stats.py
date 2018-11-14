from codewatch import Stats


def test_can_insert_and_retrieve_value():
    stats = Stats()
    stats.append('abc', 123)
    assert stats.get('abc') == 123


def test_stats_string_representations_same_as_underlying_dict():
    underyling_dict = {
        'key1': 'val1',
        'key2': [1, 2, 3],
        'key3': {},
    }
    stats = Stats(underyling_dict)
    assert stats.__repr__() == underyling_dict.__repr__()
    assert stats.__str__() == underyling_dict.__str__()


def test_append_list():
    stats = Stats()
    stats.append_list('mylist', 1)
    stats.append_list('mylist', 2)
    stats.append_list('mylist', 3)
    assert stats.get('mylist', [1, 2, 3])


def test_increment():
    stats = Stats()
    stats.increment('mycounter')
    assert stats.get('mycounter', 1)
    stats.increment('mycounter')
    assert stats.get('mycounter', 2)


def test_append():
    stats = Stats()

    mydict = {1: 2}
    stats.append('mydict', mydict)
    mylist = [1, 2, 3]
    stats.append('mylist', mylist)

    assert stats.get('mydict', mydict)
    assert stats.get('mylist', mylist)


def test_namespaced():
    stats = Stats()
    stats.append('counter_level1', 1)
    stats.namespaced('level2').append('counter_level2', 2)
    stats.namespaced('level2').namespaced('level3').append(
        'counter_level3',
        3,
    )

    assert stats.get('counter_level1') == 1
    assert stats.get('level2').get('counter_level2') == 2
    assert stats.get('level2').get('level3').get('counter_level3') == 3


def test_responds_to_dict_methods():
    stats = Stats()
    stats.increment('mycounter')

    assert stats.keys() == ['mycounter']
    assert stats.values() == [1]
