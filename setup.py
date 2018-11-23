import sys
from setuptools import (
    find_packages,
    setup,
)

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
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


if sys.version_info[0:3] >= (3, 7, 0):
    # astroid<2.0 does not work on python>=3.7 because StopIteration is removed
    INSTALL_REQUIRES = [
        'astroid==2.0.4'
    ]
else:
    INSTALL_REQUIRES = [
        'astroid==1.6.4',  # 2.0 onwards is py3 only
    ]

setup(
    name='codewatch',
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    version='0.0.13',
    scripts=['bin/codewatch'],
    install_requires=INSTALL_REQUIRES,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <3.8"
 )
