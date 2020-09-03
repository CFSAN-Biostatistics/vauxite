#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 
                'ipfs-api>=0.2.3',
                'cwlref-runner>=1.0',
                'cwltool>=3.0.2',
                'frozendict>=1.2',
                'pysam>=0.16.0.1']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Justin Payne",
    author_email='justin.payne@fda.hhs.gov',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Vauxite is an in-silico sequence typing framework with its own IPFS typing schema distribution system.",
    entry_points={
        'console_scripts': [
            'vauxite=vauxite.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='vauxite',
    name='vauxite',
    packages=find_packages(include=['vauxite', 'vauxite.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/crashfrog/vauxite',
    version='0.1.0',
    zip_safe=False,
)
