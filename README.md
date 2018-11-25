<div align="center">
<a href="https://github.com/tophat/codewatch">
<img src="website/static/img/codewatch@2x.png"/>
</a>

[![version](https://img.shields.io/pypi/v/codewatch.svg)](https://pypi.org/project/codewatch/)
[![codecov](https://codecov.io/gh/tophat/codewatch/branch/master/graph/badge.svg)](https://codecov.io/gh/tophat/codewatch)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Builds](https://img.shields.io/circleci/project/github/tophat/codewatch/master.svg)](https://circleci.com/gh/tophat/codewatch)
[![Slack workspace](https://slackinvite.dev.tophat.com/badge.svg)](https://opensource.tophat.com/#join-slack)
[![Maturity badge - level 1](https://img.shields.io/badge/Maturity-Level%201%20--%20New%20Project-yellow.svg)](https://github.com/tophat/getting-started/blob/master/scorecard.md)

</div>

# Overview

_Monitor and manage deeply customizable metrics about your python code using ASTs._

codewatch lets you write simple python code to track statistics about the state of your codebase and write lint-like assertions on those statistics. Use this to incrementally improve and evolve the quality of your code base, increase the visibility of problematic code, to encourage use of new patterns while discouraging old ones, to enforce coding style guides, or to prevent certain kinds of regression errors.

# Installation
Python: 2.7, 3.6, 3.7

Execute the following in your terminal:

```bash
pip install codewatch
```

# Usage

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

# Contributing

## Helpful resources
TODO

# Contributors

Thanks goes to these wonderful people! ([Emoji key](https://github.com/kentcdodds/all-contributors#emoji-key))

| [<img src="https://avatars2.githubusercontent.com/u/9436142?s=460&v=4" width="100px;"/><br /><sub><b>Josh Doncaster Marsiglio</b></sub>](https://github.com/lime-green)<br />[💻](https://github.com/tophat/codewatch/commits?author=lime-green)  | [<img src="https://avatars0.githubusercontent.com/u/18485117?s=460&v=4" width="100px;"/><br /><sub><b>Rohit Jain</b></sub>](https://github.com/rohit-jain27)<br />[💻](https://github.com/tophat/codewatch/commits?author=rohitjain-27) | [<img src="https://avatars2.githubusercontent.com/u/840172?s=460&v=4" width="100px;"/><br /><sub><b>Chris Abiad</b></sub>](https://github.com/cabiad)<br />[💻](https://github.com/tophat/codewatch/commits?author=cabiad) |
| :---: | :---: | :---: |
| [<img src="https://avatars.githubusercontent.com/u/3876970?s=100" width="100px;"/><br /><sub><b>Francois Campbell</b></sub>](https://github.com/francoiscampbell)<br />🤔 | [<img src="https://avatars3.githubusercontent.com/u/8105535?s=100" width="100px;"/><br /><sub><b>Monica Moore</b></sub>](https://github.com/monicamm95)<br />🎨 | |
| [<img src="https://avatars.githubusercontent.com/u/3534236?s=100" width="100px;"/><br /><sub><b>Jake Bolam</b></sub>](https://github.com/jakebolam)<br />[🚇](https://github.com/tophat/codewatch/commits?author=jakebolam) | [<img src="https://avatars0.githubusercontent.com/u/6020693?s=100" width="100px;"/><br /><sub><b>Shouvik D'Costa</b></sub>](https://github.com/sdcosta)<br />[🚇](https://github.com/tophat/codewatch/commits?author=sdcosta) | [<img src="https://avatars1.githubusercontent.com/u/445636?s=100" width="100px;"/><br /><sub><b>Siavash Bidgoly</b></sub>](https://github.com/syavash)<br />[🚇](https://github.com/tophat/codewatch/commits?author=syavash) |

# Credits

Special thanks to [Carol Skelly](https://github.com/iatek) for donating the 'tophat' GitHub organization.
