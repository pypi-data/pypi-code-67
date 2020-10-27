#  Copyright (c) 2015-2018 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
"""Base Linter Module."""

import abc

from molecule import util


class Base(object):
    """Base Linter Class."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        """
        Initialize code for all :ref:`Lint` classes.

        :param config: An instance of a Molecule config.
        :returns: None
        """
        self._config = config

    @abc.abstractproperty
    def default_options(self):  # pragma: no cover
        """
        Provide Default CLI arguments to ``cmd`` and returns a dict.

        :return: dict
        """

    @abc.abstractproperty
    def default_env(self):  # pragma: no cover
        """
        Provide default env variables to ``cmd`` and returns a dict.

        :return: dict
        """

    @abc.abstractmethod
    def execute(self):  # pragma: no cover
        """
        Execute ``cmd`` and returns None.

        :return: None
        """

    @property
    def name(self):
        """
        Name of the lint and returns a string.

        :returns: str
        """
        return self._config.config["lint"]

    @property
    def enabled(self):
        return self._config.config["lint"]

    @property
    def options(self):
        return self.default_options

    @property
    def env(self):
        return util.merge_dicts(self.default_env)
