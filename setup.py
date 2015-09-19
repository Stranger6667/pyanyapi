#!/usr/bin/env python
# coding: utf-8
import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


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


requirements = [
    'lxml',
]

test_requirements = [
    'pytest>=2.5.0',
    'pytest-cov>=1.7',
    'coverage==3.7.1',
]

if sys.version_info < (3, 3):
    test_requirements.append('mock==1.0.1')

setup(
    name='pyanyapi',
    version='0.1',
    packages=['pyanyapi'],
    license='MIT',
    author='Dmitry Dygalo',
    author_email='dadygalo@gmail.com',
    description='',
    classifiers=[
        'Development Status :: 3 - Alpha',
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
    ],
    cmdclass={'test': PyTest},
    include_package_data=True,
    install_requires=requirements,
    tests_require=test_requirements
)