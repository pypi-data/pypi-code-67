#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2020, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
import itertools
import re
import warnings
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    Union,
)

# External imports
from typing_extensions import Literal

# Bokeh imports
from ..models import HoverTool, Plot, Tool, Toolbar
from ..models.tools import Drag, Inspection, Scroll, Tap

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'process_active_tools',
    'process_tools_arg',
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

# TODO: str should be literal union of e.g. pan | xpan | ypan
Auto = Literal["auto"]
ActiveDrag = Union[Drag, Auto, str, None]
ActiveInspect = Union[List[Inspection], Inspection, Auto, str, None]
ActiveScroll = Union[Scroll, Auto, str, None]
ActiveTap = Union[Tap, Auto, str, None]

def process_active_tools(toolbar: Toolbar, tool_map: Dict[str, Tool],
        active_drag: ActiveDrag, active_inspect: ActiveInspect, active_scroll: ActiveScroll, active_tap: ActiveTap) -> None:
    """ Adds tools to the plot object

    Args:
        toolbar (Toolbar): instance of a Toolbar object
        tools_map (dict[str]): tool_map from _process_tools_arg
        active_drag (str or Tool): the tool to set active for drag
        active_inspect (str or Tool): the tool to set active for inspect
        active_scroll (str or Tool): the tool to set active for scroll
        active_tap (str or Tool): the tool to set active for tap

    Returns:
        None

    Note:
        This function sets properties on Toolbar
    """
    if active_drag in ['auto', None] or isinstance(active_drag, Tool):
        toolbar.active_drag = active_drag
    elif active_drag in tool_map:
        toolbar.active_drag = tool_map[active_drag]
    else:
        raise ValueError("Got unknown %r for 'active_drag', which was not a string supplied in 'tools' argument" % active_drag)

    if active_inspect in ["auto", None] or isinstance(active_inspect, Tool) or \
            (isinstance(active_inspect, list) and all(isinstance(t, Tool) for t in active_inspect)):
        toolbar.active_inspect = active_inspect
    elif isinstance(active_inspect, str) and active_inspect in tool_map:
        toolbar.active_inspect = tool_map[active_inspect]
    else:
        raise ValueError("Got unknown %r for 'active_inspect', which was not a string supplied in 'tools' argument" % active_scroll)

    if active_scroll in ['auto', None] or isinstance(active_scroll, Tool):
        toolbar.active_scroll = active_scroll
    elif active_scroll in tool_map:
        toolbar.active_scroll = tool_map[active_scroll]
    else:
        raise ValueError("Got unknown %r for 'active_scroll', which was not a string supplied in 'tools' argument" % active_scroll)

    if active_tap in ['auto', None] or isinstance(active_tap, Tool):
        toolbar.active_tap = active_tap
    elif active_tap in tool_map:
        toolbar.active_tap = tool_map[active_tap]
    else:
        raise ValueError("Got unknown %r for 'active_tap', which was not a string supplied in 'tools' argument" % active_tap)

def process_tools_arg(plot: Plot, tools: Union[str, Sequence[Union[Tool, str]]],
        tooltips: Optional[Union[str, Tuple[str, str]]] = None) -> Tuple[List[Tool], Dict[str, Tool]]:
    """ Adds tools to the plot object

    Args:
        plot (Plot): instance of a plot object

        tools (seq[Tool or str]|str): list of tool types or string listing the
            tool names. Those are converted using the to actual Tool instances.

        tooltips (string or seq[tuple[str, str]], optional):
            tooltips to use to configure a HoverTool

    Returns:
        list of Tools objects added to plot, map of supplied string names to tools
    """
    tool_objs, tool_map = _resolve_tools(tools)

    repeated_tools = [ str(obj) for obj in _collect_repeated_tools(tool_objs) ]
    if repeated_tools:
        warnings.warn("%s are being repeated" % ",".join(repeated_tools))

    if tooltips is not None:
        for tool_obj in tool_objs:
            if isinstance(tool_obj, HoverTool):
                tool_obj.tooltips = tooltips
                break
        else:
            tool_objs.append(HoverTool(tooltips=tooltips)) # type: ignore

    return tool_objs, tool_map

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

def _resolve_tools(tools: Union[str, Sequence[Union[Tool, str]]]) -> Tuple[List[Tool], Dict[str, Tool]]:
    tool_objs = []
    tool_map = {}

    if not isinstance(tools, str):
        temp_tool_str = ""
        for tool in tools:
            if isinstance(tool, Tool):
                tool_objs.append(tool)
            elif isinstance(tool, str):
                temp_tool_str += tool + ','
            else:
                raise ValueError("tool should be a string or an instance of Tool class")
        tools = temp_tool_str

    for tool in re.split(r"\s*,\s*", tools.strip()):
        # re.split will return empty strings; ignore them.
        if tool == "":
            continue

        tool_obj = Tool.from_string(tool)
        tool_objs.append(tool_obj)
        tool_map[tool] = tool_obj

    return tool_objs, tool_map

def _collect_repeated_tools(tool_objs: List[Tool]) -> Iterator[Tool]:
    class Item(NamedTuple):
        obj: Tool
        properties: Dict[str, Any]

    key = lambda obj: obj.__class__.__name__

    for _, group in itertools.groupby(sorted(tool_objs, key=key), key=key):
        rest = [ Item(obj, obj.properties_with_values()) for obj in group ]
        while len(rest) > 1:
            head, *rest = rest
            for item in rest:
                if item.properties == head.properties:
                    yield item.obj

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
