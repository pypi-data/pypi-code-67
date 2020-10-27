#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['record_api']

package_data = \
{'': ['*']}

install_requires = \
['tqdm',
 'networkx',
 'orjson',
 'black',
 'pydantic',
 'typing_extensions',
 'libcst']

extras_require = \
{'test': ['pytest', 'numpy', 'pandas']}

entry_points = \
{'pytest11': ['record_api = record_api.pytest_plugin']}

setup(name='record_api',
      version='1.3.0',
      description='Records APIs of Python programs',
      author='Saul Shanabrook',
      author_email='s.shanabrook@gmail.com',
      url='https://github.com/quansight-labs/python_record_api',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
      entry_points=entry_points,
     )
