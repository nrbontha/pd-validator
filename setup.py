#!/usr/bin/env python2

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# get long description from README
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pd_validator',  
    version='1.0.0',  
    description='pandas DataFrame validation library',  
    long_description=long_description,  
    long_description_content_type='text/markdown', 
    url='https://github.com/nrbontha/pd-validator', 
    author='nrbontha',  
    author_email='nrbontha@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Data Validation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords=['pandas', 'data', 'validation', 'analysis'],  
    packages=find_packages(exclude=['contrib', 'docs']), 
    install_requires=['pandas', 'numpy']
)

