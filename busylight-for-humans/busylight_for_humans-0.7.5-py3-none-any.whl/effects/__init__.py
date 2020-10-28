""" Effects

"""

import asyncio
import time

from itertools import cycle
from typing import Callable, Dict, List, Tuple, Union

from .gradient import Gradient
from .spectrum import Spectrum

from ..lights import USBLight, USBLightIOError

## Effects are called from a threading.Thread.run subclass
## that can be stopped externally. The effects functions
## need to yield ocassionlly to allow the thread to decide
## whether it has been stopped or not. The more often the
## effect yields, the better the application will respond
## to user input.


def rainbow(light: USBLight, interval: float = 0.05, **kwds) -> None:
    """Color cycle the light thru a rainbow spectrum.

    :param light: USBLight
    :param interval: float
    """
    colors = [rgb for rgb in Spectrum(steps=255)]
    while True:
        for color in cycle(colors):
            try:
                light.on(color)
            except USBLightIOError:
                exit()
            yield
            time.sleep(interval)


async def rainbow_async(USBLight: object, interval: float = 0.05, **kwds) -> None:
    """Color cycle the light thru a rainbow spectrum.

    :param light: USBLight
    :param interval: float
    """
    colors = [rgb for rgb in Spectrum(steps=255)]
    while True:
        for color in cycle(colors):
            try:
                light.on(color)
            except USBLightIOError:
                exit()
            yield
            await asyncio.sleep(interval)


def pulse(
    light: USBLight,
    color: Tuple[int, int, int] = None,
    interval: float = 0.01,
) -> None:
    """Pulse the light with scaled values of the supplied `color`.

    If no color is supplied or the color is black (0,0,0), the function defaults
    to the color red (255, 0, 0).

    :param light: USBLight
    :param color: Tuple[int, int, int]
    :param interval: float
    """
    if not color or not any(color):
        color = (255, 0, 0)

    r, g, b = color

    gradient = Gradient(color, 8, reverse=True)

    while True:
        for color in cycle(gradient):
            try:
                light.on(color)
            except USBLightIOError:
                exit()
            yield
            time.sleep(interval)


async def pulse_async(
    light: USBLight,
    color: Tuple[int, int, int],
    interval: float = 0.1,
) -> None:
    """
    :param light: USBLight
    :param color: Tuple[int, int, int]
    :param interval: float
    """

    if not color or not any(color):
        color = (255, 0, 0)

    r, g, b = color

    gradient = Gradient(color, 8, reverse=True)

    while True:
        for color in cycle(gradient):
            try:
                light.on(color)
            except USBLightIOError:
                exit()
            yield
            await asyncio.sleep(interval)


def flash_lights_impressively(
    light: USBLight,
    colors: List[Tuple[int, int, int]] = None,
    interval: float = 0.05,
    **kwds
) -> None:
    """Alternate between given colors very quickly.

    If no colors are given, defaults to [red, green, blue].

    :param light: USBLight
    :param colors: List[Tuple[int, int, int]]
    :param interval: float
    """
    if not colors:
        colors = [(0xFF, 0, 0), (0, 0xFF, 0), (0, 0, 0xFF)]

    for color in cycle(colors):
        try:
            light.on(color)
        except USBLightIOError:
            exit()
        yield
        time.sleep(interval)


async def flash_lights_impressively_async(
    light: USBLight, colors: List[Tuple[int, int, int]], interval: float = 0.1
) -> None:
    """Alternate between given colors very quickly.

    If no colors are given, defaults to [red, green, blue].

    :param light: USBLight
    :param colors: List[Tuple[int, int, int]]
    :param interval: float
    """

    if not colors:
        colors = [(0xFF, 0, 0), (0, 0xFF, 0), (0, 0, 0xFF)]

    for color in cycle(colors):
        try:
            light.on(color)
        except USBLightIOError:
            exit()
        yield
        await asyncio.sleep(interval)


__all__ = [
    "Gradient",
    "Spectrum",
    "rainbow",
    "rainbow_async",
    "pulse",
    "pulse_async",
    "flash_lights_impressively",
    "flash_lights_impressively_async",
]
