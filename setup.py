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
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Libraries ",
]


INSTALL_REQUIRES = [
    'astroid==2.0.4; python_version>="3"',
    'astroid==1.6.4; python_version<"3"',  # 2.0 onwards is py3 only
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
    version='0.1.0',
    description="Monitor and manage deeply customizable metrics about your python code using ASTs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tophat/codewatch",
    scripts=['bin/codewatch'],
    install_requires=INSTALL_REQUIRES,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <3.8"
 )
