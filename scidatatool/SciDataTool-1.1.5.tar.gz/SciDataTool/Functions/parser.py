# -*- coding: utf-8 -*-
from numpy import pi, sqrt, inf  # for eval
from SciDataTool.Functions import AxisError
from SciDataTool.Classes.RequestedAxis import RequestedAxis


def read_input_strings(args, axis_data):
    """Reads the string input into the "get_along" methods to define the axes
    Parameters
    ----------
    args: list
        list of string describing the requested axes
    axis_data: ndarray
        user-input values for the axes
    Returns
    -------
    list of axes data (axes_list)
    """
    axes_list = []
    for axis_str in args:
        unit = "SI"
        values = None
        indices = None
        input_data = None
        # Detect unit
        if "{" in axis_str:
            elems = axis_str.split("{")
            unit = elems[1].strip("}")
            axis_str = elems[0]
        # Detect normalization
        if "->" in axis_str:
            elems = axis_str.split("->")
            if "=" in axis_str:
                unit = elems[1].split("=")[0]
            elif "[" in axis_str:
                unit = elems[1].split("[")[0]
            else:
                unit = elems[1]
            name = elems[0]
            axis_str = axis_str.replace("->" + unit, "")
        # Detect sum
        if "sum" in axis_str:
            elems = axis_str.split("=sum")
            name = elems[0]
            extension = "sum"
        elif "oneperiod" in axis_str:
            elems = axis_str.split("[")
            name = elems[0]
            extension = "oneperiod"
        elif "antiperiod" in axis_str:
            elems = axis_str.split("[")
            name = elems[0]
            extension = "antiperiod"
        elif "smallestperiod" in axis_str:
            elems = axis_str.split("[")
            name = elems[0]
            extension = "smallestperiod"
        # Detect axis_data input
        elif "axis_data" in axis_str:
            elems = axis_str.split("=axis_data")
            name = elems[0]
            extension = "axis_data"
            try:
                input_data = axis_data[name]
            except:
                raise AxisError("ERROR: No axis_data provided")
        # Detect above
        elif ">" in axis_str:
            elems = axis_str.split(">")
            init_str = elems[1]
            interval_init = eval(init_str)
            interval_final = inf
            name = elems[0]
            extension = "interval"
            input_data = [interval_init, interval_final]
        # Detect below
        elif "<" in axis_str:
            elems = axis_str.split("<")
            init_str = elems[1]
            interval_init = -inf
            interval_final = eval(init_str)
            name = elems[0]
            extension = "interval"
            input_data = [interval_init, interval_final]
        # Detect interval
        elif "=[" in axis_str:
            elems = axis_str.split("=[")
            elems2 = elems[1].split(",")
            init_str = elems2[0]
            interval_init = eval(init_str)
            final_str = elems2[1].strip("]")
            interval_final = eval(final_str)
            name = elems[0]
            extension = "interval"
            input_data = [interval_init, interval_final]
        # Detect single value
        elif "=" in axis_str:
            elems = axis_str.split("=")
            name = elems[0]
            extension = "single"
            input_data = [eval(elems[1])]
        # Detect index input...
        elif "[" in axis_str:
            elems = axis_str.split("[")
            ind_str = elems[1].strip("]")
            name = elems[0]
            # Range of indices
            if ":" in ind_str:
                elems2 = ind_str.split(":")
                extension = "interval"
                indices = [i for i in range(int(elems2[0]), int(elems2[1]) + 1)]
            # List of indices
            elif "," in ind_str:
                extension = "list"
                indices = [int(x) for x in ind_str.split(",")]
            # Single index
            else:
                extension = "single"
                indices = [int(ind_str)]
        # Whole axis
        else:
            name = axis_str
            extension = "whole"
        # RequestedAxis object creation
        axis = RequestedAxis(
            name=name,
            unit=unit,
            extension=extension,
            values=values,
            indices=indices,
            input_data=input_data,
        )
        axes_list.append(axis)
    return axes_list
