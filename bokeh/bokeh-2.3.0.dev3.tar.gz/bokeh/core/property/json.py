#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2020, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
''' Provide the JSON property.

'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Bokeh imports
from .primitive import String

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'JSON',
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

class JSON(String):
    ''' Accept JSON string values.

    The value is transmitted and received by BokehJS as a *string*
    containing JSON content. i.e., you must use ``JSON.parse`` to unpack
    the value into a JavaScript hash.

    Args:
        default (string or None, optional) :
            A default value for attributes created from this property to
            have (default: None)

        help (str or None, optional) :
            A documentation string for this property. It will be automatically
            used by the :ref:`bokeh.sphinxext.bokeh_prop` extension when
            generating Spinx documentation. (default: None)

        serialized (bool, optional) :
            Whether attributes created from this property should be included
            in serialization (default: True)

        readonly (bool, optional) :
            Whether attributes created from this property are read-only.
            (default: False)

    '''
    def validate(self, value, detail=True):
        super().validate(value, detail)

        if value is None: return

        try:
            import json
            json.loads(value)
        except ValueError:
            msg = "" if not detail else "expected JSON text, got %r" % value
            raise ValueError(msg)

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
