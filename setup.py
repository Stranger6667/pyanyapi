#!/usr/bin/env python
# coding: utf-8
import os
import platform
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


PYPY = hasattr(sys, 'pypy_translation_info')
PYPY3 = PYPY and sys.version_info[0] == 3
JYTHON = platform.system() == 'Java'


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        sys.path.insert(0, os.path.dirname(__file__))

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


requirements = ['PyYAML==3.11']
test_requirements = ['pytest==2.8.0']


if sys.version_info < (3, 3):
    test_requirements.append('mock==1.0.1')
if sys.version_info[:2] == (3, 2):
    test_requirements.append('coverage==3.7.1')

if not JYTHON:
    if not PYPY:
        requirements.append('ujson')
    if not PYPY3:
        requirements.append('lxml')
    test_requirements.append('pytest-cov==1.8')


setup(
    name='pyanyapi',
    url='https://github.com/Stranger6667/pyanyapi',
    version='0.4',
    packages=['pyanyapi'],
    license='MIT',
    author='Dmitry Dygalo',
    author_email='dadygalo@gmail.com',
    maintainer='Dmitry Dygalo',
    maintainer_email='dadygalo@gmail.com',
    keywords=['parsing', 'interface', 'xml', 'json', 'yaml', 'API', 'XPath', 'regexp'],
    description='Tools for convenient interface creation over various types of data in declarative way.',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Jython',
        'Topic :: Text Processing :: General',
        'Topic :: Utilities',
    ],
    cmdclass={'test': PyTest},
    include_package_data=True,
    install_requires=requirements,
    tests_require=test_requirements
)
