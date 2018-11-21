from setuptools import (
    find_packages,
    setup,
)

setup(
    name='codewatch',
    packages=find_packages(),
    version='0.0.3',
    scripts=['bin/codewatch'],
    install_requires=[
        'astroid==1.6.4',  # 2.0 onwards is py3 only
    ],
 )
