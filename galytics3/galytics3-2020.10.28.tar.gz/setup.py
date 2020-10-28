#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import re

with open("README.md", "r", encoding="utf8") as fh:
    readme = fh.read()

package = "galytics3"


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)


setup(
    name="galytics3",
    version=get_version(package),
    description="Обертка над библиотекой google_api_python_client для работы с API Google Analytics v3",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Pavel Maksimov",
    author_email="vur21@ya.ru",
    url="https://github.com/pavelmaksimov/galytics3",
    install_requires=['pandas', 'google_api_python_client', 'oauth2client'],
    packages=[package],
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords="google,analytics,api,client,python",
    test_suite="tests.py",
)
