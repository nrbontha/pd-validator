#!/usr/bin/env python

import setuptools
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# get long description from README
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="pd_validator",
    version="1.0.0",
    author="nrbontha",
    author_email="nrbontha@gmail.com",
    description="pandas DataFrame validation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nrbontha/pd-validator",
    install_requires=['pandas', 'numpy'],
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2"
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords=['pandas', 'data', 'validation', 'analysis']
)
