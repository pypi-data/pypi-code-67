# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['RPA', 'RPA.core', 'RPA.core.locators']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=7.0.0,<8.0.0', 'selenium>=3.141.0,<4.0.0', 'webdrivermanager>=0.7.4']

setup_kwargs = {
    'name': 'rpaframework-core',
    'version': '2.1.2',
    'description': 'Core utilities used by RPA Framework',
    'long_description': 'rpaframework-core\n=================\n\nThis package is a set of core functionality and utilities used\nby `RPA Framework`_. It is not intended to be installed directly, but\nas a dependency to other projects.\n\n.. _RPA Framework: https://rpaframework.org\n',
    'author': 'RPA Framework',
    'author_email': 'rpafw@robocorp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rpaframework.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
