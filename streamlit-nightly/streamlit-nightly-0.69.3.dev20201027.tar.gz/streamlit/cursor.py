# Copyright 2018-2020 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, Tuple, Any

from streamlit.report_thread import get_report_ctx

# A "CursorPath" is a variable-length tuple of ints.
CursorPath = Tuple[int, ...]


def get_container_cursor(container) -> Optional["Cursor"]:
    ctx = get_report_ctx()

    if ctx is None:
        return None

    if container in ctx.cursors:
        return ctx.cursors[container]

    cursor = RunningCursor()
    ctx.cursors[container] = cursor
    return cursor


class Cursor:
    """A pointer to a location in the app.

    When adding an element to the app, you should always call
    get_locked_cursor() on that element's respective Cursor.
    """

    @property
    def index(self) -> int:
        raise NotImplementedError()

    @property
    def path(self) -> CursorPath:
        raise NotImplementedError()

    @property
    def is_locked(self) -> bool:
        raise NotImplementedError()

    def get_locked_cursor(self, **props) -> "LockedCursor":
        raise NotImplementedError()

    @property
    def props(self) -> Any:
        """Other data in this cursor. This is a temporary measure that will go
        away when we implement improved return values for elements.

        This is only implemented in LockedCursor.
        """
        raise NotImplementedError()


class RunningCursor(Cursor):
    def __init__(self, path: CursorPath = ()):
        """A moving pointer to a location in the app.

        RunningCursors auto-increment to the next available location when you
        call get_locked_cursor() on them.

        Parameters
        ----------
        path: tuple of ints
          The full path of this cursor, consisting of the IDs of all ancestors. The
          0th item is the topmost ancestor.

        """
        self._index = 0
        self._path = path

    @property
    def index(self) -> int:
        return self._index

    @property
    def path(self) -> CursorPath:
        return self._path

    @property
    def is_locked(self) -> bool:
        return False

    def get_locked_cursor(self, **props) -> "LockedCursor":
        locked_cursor = LockedCursor(path=self._path, index=self._index, **props)

        self._index += 1

        return locked_cursor


class LockedCursor(Cursor):
    def __init__(self, path: CursorPath = (), index: int = 0, **props):
        """A locked pointer to a location in the app.

        LockedCursors always point to the same location, even when you call
        get_locked_cursor() on them.

        Parameters
        ----------
        path: tuple of ints
          The full path of this cursor, consisting of the IDs of all ancestors. The
          0th item is the topmost ancestor.
        index: int
        **props: any
          Anything else you want to store in this cursor. This is a temporary
          measure that will go away when we implement improved return values
          for elements.

        """
        self._index = index
        self._path = path
        self._props = props

    @property
    def index(self) -> int:
        return self._index

    @property
    def path(self) -> CursorPath:
        return self._path

    @property
    def is_locked(self) -> bool:
        return True

    def get_locked_cursor(self, **props) -> "LockedCursor":
        self._props = props
        return self

    @property
    def props(self) -> Any:
        return self._props
