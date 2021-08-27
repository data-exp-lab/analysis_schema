#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pydantic', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['Click>=6.0', 'pytest', ]

setup(
    author="Matthew Turk",
    author_email='matthewturk@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Declarative schema for analysis of physical systems",
    entry_points={
        'console_scripts': [
            'analysis_schema=analysis_schema.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='analysis_schema',
    name='analysis_schema',
    packages=find_packages(include=['analysis_schema']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/data-exp-lab/analysis_schema/',
    version='0.1.0',
    zip_safe=False,
)
