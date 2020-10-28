# $Id: __init__.py 8376 2019-08-27 19:49:29Z milde $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

# Internationalization details are documented in
# <http://docutils.sf.net/docs/howto/i18n.html>.

"""
This package contains modules for language-dependent features of
reStructuredText.
"""

__docformat__ = 'reStructuredText'

import sys

from docutils.utils import normalize_language_tag


_languages = {}

def get_language(language_code):
    for tag in normalize_language_tag(language_code):
        tag = tag.replace('-', '_') # '-' not valid in module names
        if tag in _languages:
            return _languages[tag]
        try:
            module = __import__(tag, globals(), locals(), level=1)
        except ImportError:
            try:
                module = __import__(tag, globals(), locals(), level=0)
            except ImportError:
                continue
        _languages[tag] = module
        return module
    return None
