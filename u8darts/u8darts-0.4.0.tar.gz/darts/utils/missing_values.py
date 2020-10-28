"""
Utils for filling missing values
--------------------------------
"""

from darts.timeseries import TimeSeries
from darts.logging import get_logger, raise_if, raise_if_not

from typing import Union

logger = get_logger(__name__)


def missing_values_ratio(series: TimeSeries) -> float:
    """
    Computes the ratio of missing values

    Parameters
    ----------
    series
        The time series to compute ratio on

    Returns
    -------
    float
        The ratio of missing values
    """

    return series.pd_dataframe().isnull().sum().mean() / len(series)


def fill_missing_values(series: TimeSeries, fill: Union[str, float] = 'auto', **interpolate_kwargs) -> TimeSeries:
    """
    Fills missing values in the provided time series

    Parameters
    ----------
    series
        The time series for which to fill missing values
    fill
        The value used to replace the missing values.
        If set to 'auto', will auto-fill missing values using the `pandas.Dataframe.interpolate()` method.
    interpolate_kwargs
        Keyword arguments for `pandas.Dataframe.interpolate()`, only used when fit is set to 'auto'.
        See `the documentation
        <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.interpolate.html>`_
        for the list of supported parameters.

    Returns
    -------
    TimeSeries
        A new TimeSeries with all missing values filled according to the rules above.
    """
    raise_if_not(isinstance(fill, str) or isinstance(fill, float),
                 "`fill` should either be a string or a float",
                 logger)
    raise_if(isinstance(fill, str) and fill != 'auto',
             "invalid string for `fill`: can only be set to 'auto'",
             logger)

    if fill == 'auto':
        return _auto_fill(series, **interpolate_kwargs)
    return _const_fill(series, fill)


def _const_fill(series: TimeSeries, fill: float = 0) -> TimeSeries:
    """
    Fills the missing values of `series` with only the value provided (default zeroes).

    Parameters
    ----------
    series
        The TimeSeries to check for missing values.
    fill
        The value used to replace the missing values.

    Returns
    -------
    TimeSeries
        A TimeSeries, `series` with all missing values set to `fill`.
    """

    return TimeSeries.from_times_and_values(series.time_index(),
                                            series.pd_dataframe().fillna(value=fill),
                                            series.freq())


def _auto_fill(series: TimeSeries, **interpolate_kwargs) -> TimeSeries:
    """
    This function fills the missing values in the TimeSeries `series`,
    using the `pandas.Dataframe.interpolate()` method.

    Parameters
    ----------
    series
        The time series
    interpolate_kwargs
        Keyword arguments for `pandas.Dataframe.interpolate()`.
        See `the documentation
        <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.interpolate.html>`_
        for the list of supported parameters.
    Returns
    -------
    TimeSeries
        A new TimeSeries with all missing values filled according to the rules above.
    """

    series_temp = series.pd_dataframe()

    # pandas interpolate wrapper, with chosen `method`
    if 'limit_direction' not in interpolate_kwargs:
        interpolate_kwargs['limit_direction'] = 'both'
    interpolate_kwargs['inplace'] = True
    series_temp.interpolate(**interpolate_kwargs)

    return TimeSeries.from_times_and_values(series.time_index(), series_temp.values, series.freq())
