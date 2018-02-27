#!/usr/bin/env python

from setuptools import setup
import sys

__VERSION__ = '0.0.7'

assert sys.version_info[0] == 3, "We require Python > 3"

setup(
    name='bookiesports',
    version=__VERSION__,
    description=(
        'Sports module for bookied'
    ),
    long_description=open('README.md').read(),
    download_url='https://github.com/pbsa/bookiesports/tarball/' + __VERSION__,
    author='Fabian Schuh',
    author_email='Fabian.Schuh@BlockchainProjectsBV.com',
    maintainer='Fabian Schuh',
    maintainer_email='Fabian.Schuh@BlockchainProjectsBV.com',
    url='http://pbsa.info',
    keywords=['peerplays', 'bookie'],
    packages=[
        "bookiesports",
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    entry_points={},
    install_requires=[
        "pyyaml",
        "jsonschema",
        "colorlog",
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
)
