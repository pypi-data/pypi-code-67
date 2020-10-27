#!/usr/bin/env python3
#
#  utils.py
"""
Utility functions.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import os
from types import ModuleType
from typing import IO, List

# 3rd party
import click
from domdf_python_tools.import_tools import discover, discover_entry_points
from domdf_python_tools.terminal_colours import Fore

__all__ = [
		"get_env_vars",
		"is_command",
		"import_commands",
		"abort",
		"overtype",
		]


def get_env_vars(ctx, args, incomplete):
	return [k for k in os.environ.keys() if incomplete in k]


def is_command(obj) -> bool:
	"""
	Return whether ``obj`` is a click command.

	:param obj:
	"""

	return isinstance(obj, click.Command)


def import_commands(source: ModuleType, entry_point: str) -> List[click.Command]:
	"""
	Returns a list of all commands.

	Commands can be defined locally in the module given in ``source``,
	or by third party extensions who define an entry point in the following format:

	::

		<name (can be anything)> = <module name>:<command>

	:param source:
	:param entry_point:
	"""

	local_commands = discover(source, is_command, exclude_side_effects=False)
	third_party_commands = discover_entry_points(entry_point, is_command)
	return [*local_commands, *third_party_commands]


def abort(message: str) -> Exception:
	"""
	Aborts the program execution.

	:param message:
	"""

	click.echo(Fore.RED(message), err=True)
	return click.Abort()


def overtype(*objects, sep: str = ' ', end: str = '', file: IO = None, flush: bool = False) -> None:
	"""
	Print ``objects`` to the text stream ``file``, starting with ``"\\r"``, separated by ``sep``
	and followed by ``end``.

	``sep``, ``end``, ``file`` and ``flush``, if present, must be given as keyword arguments

	All non-keyword arguments are converted to strings like :class:`str` does and written to the stream,
	separated by `sep` and followed by `end`.

	If no objects are given, :func:`~domdf_python_tools.terminal.overtype` will just write ``"\\r"``.

	.. TODO:: This does not currently work in the PyCharm console, at least on Windows

	:param objects: A list of strings or string-like objects to write to the terminal.
	:param sep: String to separate the objects with.
	:param end: String to end with.
	:param file: An object with a ``write(string)`` method.
	:default file: ``sys.stdout``
	:param flush: If :py:obj:`True`, the stream is forcibly flushed.
	"""  # noqa D400

	object0 = f"\r{objects[0]}"
	objects = (object0, *objects[1:])
	print(*objects, sep=sep, end=end, file=file, flush=flush)
