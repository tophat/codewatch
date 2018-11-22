---
id: usage
title: Usage
---

`codewatch codewatch_config_module`

`codewatch_config_module` is a file that should contain the following two methods:

*1. Visit all directories:*

```python
def directory_filter(_dir_name):
    return True
```

*2. Visit all files:*
```python
def file_filter(_file_name):
    return True
```

Tune these filters to suit your needs.

Then, you should use the `@visit` decorator. It follows a similar API to `ast.NodeVisitor`:

```python
from codewatch import visitor


def _count_import(stats):
    stats.increment('total_imports_num')

@visit('import')
def count_import(self, node):
    _count_import(self.stats)

@visit('importFrom')
def count_import_from(self, node):
    _count_import(self.stats)
```

This will build a stats dictionary that contains something like the following:

```json
{
    "total_imports_num": 763
}
```

Then, once again in the `codewatch_config_module` you can add assertions against this stat dictionary using the `@assertion` decorator

```python
from codewatch import assertion


@assertion()
def number_of_imports_not_too_high(stats):
    threshold = 700
    newStat = stats.get('total_imports_num')
    err = 'There were {} total imports detected which exceeds threshold of {}'.format(newStat, threshold)
    return newStat <= threshold, err
```

In this case, the assertion would fail since 763 is the `newStat` and the message:

```
There were 763 total imports detected which exceeds threshold of 700
```

would be printed




