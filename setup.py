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
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Libraries ",
]


setup(
    name='codewatch',
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    version='0.0.13',
    scripts=['bin/codewatch'],
    install_requires=[
        'astroid>=1.6,<2.0',  # 2.0 onwards is py3 only
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <3.7"
 )
