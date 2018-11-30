---
id: overview
title: Overview
---

[![version](https://img.shields.io/pypi/v/codewatch.svg)](https://pypi.org/project/codewatch/)
[![codecov](https://codecov.io/gh/tophat/codewatch/branch/master/graph/badge.svg)](https://codecov.io/gh/tophat/codewatch)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Builds](https://img.shields.io/circleci/project/github/tophat/codewatch/master.svg)](https://circleci.com/gh/tophat/codewatch)
[![Slack workspace](https://slackinvite.dev.tophat.com/badge.svg)](https://tophat-opensource.slack.com/)

_Monitor and manage deeply customizable metrics about your python code using ASTs._

codewatch lets you write simple python code to track statistics about the state of your codebase and write lint-like assertions on those statistics. Use this to incrementally improve and evolve the quality of your code base, increase the visibility of problematic code, to encourage use of new patterns while discouraging old ones, to enforce coding style guides, or to prevent certain kinds of regression errors.

What codewatch does:
1. Traverses your project directory
2. Parses your code into AST nodes and calls your visitor functions
3. Your visitor functions run and populate a stats dictionary
4. After all visitor functions are called, your assertion functions are called
5. Your assertion functions can assert on data in the stats dictionary, save metrics to a dashboard, or anything you can think of

# Installation
Python: >=2


Execute the following in your terminal:

```bash
pip install codewatch
```
