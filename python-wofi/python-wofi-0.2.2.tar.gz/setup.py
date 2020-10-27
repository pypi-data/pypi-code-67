# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['wofi']
setup_kwargs = {
    'name': 'python-wofi',
    'version': '0.2.2',
    'description': 'Create simple GUIs using the Wofi application',
    'long_description': '===========\npython-wofi\n===========\n\nA Python module to make simple GUIs using Wofi_.\n(forked from the original `python-rofi`_ module)\n\n.. _`python-rofi`: https://github.com/bcbnz/python-rofi\n\n.. _Wofi: https://hg.sr.ht/~scoopta/wofi\n\n\nWhat is Wofi?\n=============\n\n\nWofi is a launcher/menu program for wlroots based wayland compositors such as\nsway. Its basic operation is to display a list of options and let the user\npick one. The following screenshot is shamelessly hotlinked from the wofi\nwebsite (which you should probably visit if you want actual details about\nwofi!).\n\n.. image:: https://f.cloudninja.pw/Scaled_4.png\n   :alt: A screenshot of Wofi.\n\n.. _Wofi: https://hg.sr.ht/~scoopta/wofi\n\n\nWhat is this module?\n====================\n\nIt simplifies making simple GUIs using Wofi. It provides a class with a number\nof methods for various GUI actions (show messages, pick one of these options,\nenter some text / a number). These are translated to the appropriate Wofi\ncommand line options, and then the standard subprocess_ module is used to run\nWofi. Any output is then processed and returned to you to do whatever you like\nwith.\n\n.. _subprocess: https://docs.python.org/3/library/subprocess.html\n\n\nExamples\n--------\n\nData entry\n~~~~~~~~~~\n\nThe simplest example is to create a Wofi instance and prompt the user to enter\na piece of text::\n\n    from wofi import Wofi\n    r = Wofi()\n    name = r.text_entry(\'What is your name? \')\n\nThere are also entry methods for integers, floating-point numbers, and decimal\nnumbers::\n\n    age = r.integer_entry(\'How old are you? \')\n    height = r.float_entry(\'How tall are you? \')\n    price = r.decimal_entry(\'How much are you willing to spend? \')\n\nAll of these return the corresponding Python type. Dates and times can also be\nrequested::\n\n    dob = r.date_entry(\'What is your date of birth? \')\n    start = r.time_entry(\'When do you start work? \')\n    reminder = r.datetime_entry(\'When do you want to be alerted? \')\n\nAgain, these return the corresponding Python type. By default, they expect the\nuser to enter something in the appropriate format for the current locale. You\ncan override this by providing a list of format specifiers to any of these\nfunctions. The available specifiers are detailed in the Python documentation\nfor the datetime_ module. For example::\n\n    start = r.time_entry(\'When do you start work? \', formats=[\'%H:%M\'])\n\nAll of these entry methods are specialisations of the ``generic_entry()``\nmethod. You can use this to create your own entry types. All you need to do is\ncreate a validator function which takes the text entered by the user, and\nreturns either the Python object or an error message. For example, to enforce a\nminimum length on an entered piece of text::\n\n    validator = lambda s: (s, None) if len(s) > 6 else (None, "Too short!")\n    r.generic_entry(\'Enter a 7-character or longer string: \', validator)\n\nNote that all of these methods return ``None`` if the dialog is cancelled.\n\n.. _datetime: https://docs.python.org/3/library/datetime.html\n\nErrors\n~~~~~~\n\nTo show an error message to the user::\n\n    r.error(\'I cannot let you do that.\')\n    r.exit_with_error(\'I cannot let you do that.\')\n\nThe latter shows the error message and then exits.\n\nSelections\n~~~~~~~~~~\n\nTo give the user a list of things to select from, and return the index of the\noption they chose::\n\n    options = [\'Red\', \'Green\', \'Blue\', \'White\', \'Silver\', \'Black\', \'Other\']\n    index, key = r.select(\'What colour car do you drive?\', options)\n\nThe returned ``key`` value tells you what key the user pressed. For Enter, the\nvalue is 0, while -1 indicates they cancelled the dialog. You can also specify\ncustom key bindings::\n\n    index, key = r.select(\'What colour car do you drive?\', options, key5=(\'Alt+n\', "I don\'t drive"))\n\nIn this case, the returned ``key`` will be 5 if they press Alt+n.\n\nStatus\n~~~~~~\n\nTo display a status message to the user::\n\n    r.status("I\'m working on that...")\n\nThis is the only non-blocking method (all the others wait for the user to\nfinish before returning control to your script). To close the status message::\n\n    r.close()\n\nCalling a display or entry method will also close any status message currently\ndisplayed.\n\nMessages\n~~~~~~~~\n\nAny of the entry methods and the select method have an optional argument\n``message``. This is a string which is displayed below the prompt. The string\ncan contain Pango_ markup::\n\n    r.text_entry(\'What are your goals for this year? \', message=\'Be <b>bold</b>!\')\n\nIf you need to escape a string to avoid it being mistaken for markup, use the\n``Wofi.escape()`` class method::\n\n    msg = Wofi.escape(\'Format: <firstname> <lastname>\')\n    r.text_entry(\'Enter your name: \', message=msg)\n\n.. _Pango:  https://developer.gnome.org/pango/stable/PangoMarkupFormat.html\n\nCustomisation\n~~~~~~~~~~~~~\n\nThere are a number of options available to customise the display. These can be\nset in the initialiser to apply to every dialog displayed, or you can pass them\nto any of the display methods to change just that dialog. See the Wofi\ndocumentation for full details of these parameters.\n\n* ``lines``: The maximum number of lines to show before scrolling.\n\n* ``fixed_lines``: Keep a fixed number of lines visible.\n\n* ``width``: If positive but not more than 100, this is the percentage of the\n  screen\'s width the window takes up. If greater than 100, it is the width in\n  pixels. If negative, it estimates the width required for the corresponding\n  number of characters, i.e., -30 would set the width so approximately 30\n  characters per row would show.\n\n* ``fullscreen``: If True, use the full height and width of the screen.\n\n* ``location``:  The position of the window on the screen.\n\n* You can also pass in arbitrary arguments to wofi through the ``wofi_args``\n  parameter. These have to be passed in as a list of strings, with every\n  argument in a seperate string. For example, to make a selection case\n  insensitive::\n    \n    r = Wofi()\n    r.select(\'Choose one\', [\'option 1\', \'option 2\', \'option 3\'],\n        wofi_args=[\'-i\'])\n  \n  or, to choose a different style for an instance of ``Wofi``::\n\n    r = Wofi(wofi_args=[\'-theme\', \'path/to/theme.rasi\'])\n    r.status(\'Stuff is happening, please wait...\')\n\n\n\n\nRequirements\n============\n\nYou need to have the ``wofi`` executable available on the system path (i.e.,\ninstall Wofi!). Everything else that python-wofi needs is provided by the\nPython standard libraries.\n\n\nWhat Python versions are supported?\n===================================\n\nIt *should* work with any version of Python from 2.7 onwards. It may work with\nolder versions, though no specific support for them will be added. It is\ndeveloped on Python 2.7 and Python 3.6 -- the latest versions of the Python 2\nand 3 branches respectively.\n\n\nWhat license does it use?\n=========================\n\nThe MIT license, the same as python-wofi.\n\n\nBug reports\n===========\n\nThe project is developed on GitHub_. Please file any bug reports or feature\nrequests on the Issues_ page there.\n\n.. _GitHub: https://github.com/cristobaltapia/python-wofi\n.. _Issues: https://github.com/cristobaltapia/python-wofi/issues\n',
    'author': 'Cristóbal Tapia Camú',
    'author_email': 'crtapia@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cristobaltapia/python-wofi',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
