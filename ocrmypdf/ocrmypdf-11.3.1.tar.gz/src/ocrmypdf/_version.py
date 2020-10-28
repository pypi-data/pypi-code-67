# © 2017 James R. Barlow: github.com/jbarlow83
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pkg_resources

PROGRAM_NAME = 'ocrmypdf'

# Official PEP 396
__version__ = pkg_resources.get_distribution('ocrmypdf').version
