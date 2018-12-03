---
id: usage
title: Usage
---

`codewatch codewatch_config_module`

`codewatch_config_module` is a module that should contain your visitors, assertions and filters (if required)

### Visitors
You should use the `@visit` decorator.
The passed in node object is an [astroid](https://astroid.readthedocs.io/en/latest/) node which follows a similar API to `ast.Node`

```python
from codewatch import visit


def _count_import(stats):
    stats.increment('total_imports_num')

@visit('import')
def count_import(node, stats, _rel_file_path):
    _count_import(stats)

@visit('importFrom')
def count_import_from(node, stats, _rel_file_path):
    _count_import(stats)
```

This will build a stats dictionary that contains something like the following:

```json
{
    "total_imports_num": 763
}
```

### Assertions
Once again in the `codewatch_config_module` you can add assertions against this stat dictionary using the `@assertion` decorator

```python
from codewatch import assertion


@assertion()
def number_of_imports_not_too_high(stats):
    threshold = 700
    actual = stats.get('total_imports_num')
    err = 'There were {} total imports detected which exceeds threshold of {}'.format(actual, threshold)
    assert actual <= threshold, err
```

In this case, the assertion would fail since 763 is the `newStat` and the message:

```
There were 763 total imports detected which exceeds threshold of 700
```

would be printed

### Filters
You can add the following *optional* filters:

1. directory_filter (defaults to skip test and migration directories)

```python
# visit all directories
def directory_filter(_dir_name):
    return True
```

2. file_filter (defaults to only include python files, and skips test files)
```python
# visit all files
def file_filter(_file_name):
    return True
```

Tune these filters to suit your needs.

