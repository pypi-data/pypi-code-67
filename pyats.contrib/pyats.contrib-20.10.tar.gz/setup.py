#! /usr/bin/env python

'''Setup file for pyats.contrib

See:
    https://packaging.python.org/en/latest/distributing.html
'''

from setuptools import setup, find_packages
from os import listdir
from os.path import isfile, join

def read(path):
    with open(path) as f:
        return f.read()

def discover_creators():
    creators = filter(lambda creator: creator not in [
        '__init__.py',
        'creator.py',
        'README.md',
        'tests'
    ], listdir('src/pyats/contrib/creators'))
    creators = [creator.replace('.py', '') for creator in creators]
    return ['{source} = pyats.contrib.creators.{source}:{source_title}'
        .format(source=source, source_title=source.title()) \
            for source in creators]

# launch setup
setup(
    name = 'pyats.contrib',
    version = '20.10',

    # descriptions
    description = 'Open source package for pyATS framework extensions.',
    long_description = read('README.md'),
    long_description_content_type="text/markdown",

    # the project's main homepage.
    url = 'https://developer.cisco.com/pyats/',

    # author details
    author = 'Cisco Systems Inc.',
    author_email = 'pyats-support-ext@cisco.com',

    # project licensing
    license = 'Apache 2.0',

    classifiers = [
        'Development Status :: 6 - Mature',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # uses namespace package
    namespace_packages = ['pyats'],

    # project packages
    packages = find_packages(where = 'src'),

    # project directory
    package_dir = {
        '': 'src',
    },

    # additional package data files that goes into the package itself
    package_data = {},

    # project keywords
    keywords = 'genie pyats test automation open source contrib',

    entry_points={
        'pyats.topology.loader': discover_creators(),
        'pyats.easypy.plugins': [
            'webex = pyats.contrib.plugins.webex_plugin.webex:webex_plugin',
            'topoup = pyats.contrib.plugins.topoup_plugin.topoup:topology_up_plugin'
        ],
    },

    # package dependencies
    install_requires=[
        "ansible", "requests", "xlrd", "xlrd", "xlwt", "xlsxwriter"
    ],

    # external modules
    ext_modules = [],

    # non zip-safe (never tested it)
    zip_safe = False,
)
