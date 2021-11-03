import os
import sys
from os.path import join, exists

from setuptools import (
    find_packages,
    setup,
)

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Libraries ",
]


INSTALL_REQUIRES = [
    'astroid>=2'
]

base_dir = os.path.dirname(__file__)
readme_path = join(base_dir, 'README.md')
if exists(readme_path):
    with open(readme_path) as stream:
        long_description = stream.read()
else:
    long_description = ''

setup(
    name='codewatch',
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    version='1.0.0',
    description="Monitor and manage deeply customizable metrics about your python code using ASTs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tophat/codewatch",
    scripts=['bin/codewatch'],
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.6, <3.9"
 )
