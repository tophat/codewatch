# codewatch

WORK IN PROGRESS

## Usage

`codewatch codewatch_config_module`

The codewatch_config_module should contain the following two methods:

*1. Visit all directories:*

```python
def directory_filter(_dir_name):
    return True
```

*2. Visit all files:*
```python
def file_filter(file_name):
    return True
```

Tune these filters to suit your needs.

Then, you should add visitor classes that subclass from `codewatch.NodeVisitor`. It follows the same API as `ast.NodeVisitor`:

```python
from codewatch import NodeVisitor


class CountImportsVisitor(NodeVisitor):
    def _count_import(self):
        self.stats.increment('total_imports_num')

    def visit_Import(self, node):
        self._count_import()

    def visit_ImportFrom(self, node):
        self._count_import()
```

This will build a stats dictionary that contains something like the following:

```json
{
    "total_imports_num": 763
}
```

Then, once again in the codewatch_config_module you can add assertions against this stat dictionary. The class should inherit from `codewatch.Assertion`:

```python
from codewatch import Assertion

class CountImportsAssertion(Assertion):
    def assert_number_of_imports_not_too_high(self):
        threshold = 700
        newStat = self.stats.get('total_imports_num')
        err = 'There were {} total imports detected which exceeds threshold of {}'.format(newStat, threshold)
        return newStat <= threshold, err
```

In this case, the assertion would fail since 763 is the `newStat` and the message:

```
There were 763 total imports detected which exceeds threshold of 700
```

would be printed

## Contributing

Thanks goes to these wonderful people! ([Emoji key](https://github.com/kentcdodds/all-contributors#emoji-key))

| [<img src="https://avatars2.githubusercontent.com/u/9436142?s=460&v=4" width="100px;"/><br /><sub><b>Josh Doncaster Marsiglio</b></sub>](https://github.com/lime-green)<br />[💻](https://github.com/tophat/codewatch/commits?author=lime-green)  | [<img src="https://avatars0.githubusercontent.com/u/18485117?s=460&v=4" width="100px;"/><br /><sub><b>Rohit Jain</b></sub>](https://github.com/rohit-jain27)<br />[💻](https://github.com/tophat/codewatch/commits?author=rohitjain-27) | [<img src="https://avatars2.githubusercontent.com/u/840172?s=460&v=4" width="100px;"/><br /><sub><b>Chris Abiad</b></sub>](https://github.com/cabiad)<br />[💻](https://github.com/tophat/codewatch/commits?author=cabiad) |
| :---: | :---: | :---: |
| [<img src="https://avatars.githubusercontent.com/u/3876970?s=100"/><br /><sub><b>Francois Campbell</b></sub>](https://github.com/francoiscampbell)<br />[🤔](https://github.com/tophat/codewatch/commits?author=francoiscampbell) | | |

# Credits

Special thanks to [Carol Skelly](https://github.com/iatek) for donating the 'tophat' GitHub organization.
