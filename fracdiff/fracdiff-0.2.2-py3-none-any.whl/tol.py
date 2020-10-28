import numpy as np

from fracdiff.base import fdiff_coef


def window_from_tol_coef(n, tol_coef, max_window=2 ** 12):
    """
    Return length of window determined from tolerance to memory loss.

    Tolerance of smallness of coefficient to determine the length of window.
    That is, `window_` is chosen as the minimum integer that makes the
    absolute value of the `window`-th fracdiff coefficient is smaller than
    `tol_coef`.

    Parameters
    ----------
    - n : int
        Order of fractional differentiation.
    - tol_coef : float in range (0, 1)
        ...

    Notes
    -----
    The window for small `d` or `tol_(memory|coef)` can become extremely large.
    For instance, window grows with the order of `tol_coef ** (-1 / d)`.

    Returns
    -------
    window : int
        Length of window

    >>> window_from_tol_coef(0.5, 0.1)
    4
    >>> fdiff_coef(0.5, 3)[-1]
    -0.125
    >>> fdiff_coef(0.5, 4)[-1]
    -0.0625
    """
    coef = np.abs(fdiff_coef(n, max_window))
    return np.searchsorted(-coef, -tol_coef) + 1  # index -> length


def window_from_tol_memory(n, tol_memory, max_window=2 ** 12):
    """
    Return length of window determined from tolerance to memory loss.

    Minimum lenght of window that makes the absolute value of the sum of fracdiff
    coefficients from `window_ + 1`-th term is smaller than `tol_memory`.
    If `window` is not None, ignored.

    Notes
    -----
    The window for small `d` or `tol_(memory|coef)` can become extremely large.
    For instance, window grows with the order of `tol_coef ** (-1 / d)`.

    Parameters
    ----------
    - n : int
        Order of fractional differentiation.
    - tol_memory : float in range (0, 1)
        Tolerance of lost memory.

    >>> window_from_tol_memory(0.5, 0.2)
    9
    >>> np.sum(fdiff_coef(0.5, 10000)[9:])
    -0.19073850781678142
    >>> np.sum(fdiff_coef(0.5, 10000)[8:])
    -0.20383054883240645
    """
    lost_memory = np.abs(np.cumsum(fdiff_coef(n, max_window)))
    return np.searchsorted(-lost_memory, -tol_memory) + 1  # index -> length
