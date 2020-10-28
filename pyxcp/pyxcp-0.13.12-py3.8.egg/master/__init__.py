#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Lowlevel API reflecting available XCP services

.. note:: For technical reasons the API is split into two parts;
          common methods and a Python version specific part.

.. [1] XCP Specification, Part 2 - Protocol Layer Specification
"""

__copyright__ = """
    pySART - Simplified AUTOSAR-Toolkit for Python.

   (C) 2009-2019 by Christoph Schueler <cpu12.gems@googlemail.com>

   All Rights Reserved

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import sys

VERSION = sys.version_info
PRE35 = VERSION.major >= 3 and VERSION.minor < 5

# We need some pre-3.5 fixes, e.g. flatten() function.

if PRE35:
    from pyxcp.master.pre35 import Master
else:
    from pyxcp.master.py35 import Master
