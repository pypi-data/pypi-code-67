"""Conversion between different types of arrays"""
import numpy as np
import pyarrow as pa
import vaex.utils


supported_arrow_array_types = (pa.Array, pa.ChunkedArray)
supported_array_types = (np.ndarray, ) + supported_arrow_array_types

string_types = [pa.string(), pa.large_string()]


def filter(ar, boolean_mask):
    if isinstance(ar, supported_arrow_array_types):
        return ar.filter(pa.array(boolean_mask))
    else:
        return ar[boolean_mask]


def slice(ar, offset, length=None):
    if isinstance(ar, supported_arrow_array_types):
        return ar.slice(offset, length)
    else:
        if length is not None:
            return ar[offset:offset + length]
        else:
            return ar[offset:]


def concat(arrays):
    if len(arrays) == 1:
        return arrays[0]
    if any([isinstance(k, vaex.array_types.supported_arrow_array_types) for k in arrays]):
        return pa.chunked_array(arrays)
    else:
        ar = np.ma.concatenate(arrays)
        # avoid useless masks
        if ar.mask is False:
            ar = ar.data
        if ar.mask is np.False_:
            ar = ar.data
        return ar


def is_string_type(data_type):
    return not isinstance(data_type, np.dtype) and data_type in string_types


def is_string(ar):
    return isinstance(ar, supported_arrow_array_types) and is_string_type(ar.type)


def filter(ar, boolean_mask):
    if isinstance(ar, supported_arrow_array_types):
        return ar.filter(pa.array(boolean_mask))
    else:
        return ar[boolean_mask]


def same_type(type1, type2):
    try:
        return type1 == type2
    except TypeError:
        # numpy dtypes don't like to be compared
        return False


def tolist(ar):
    if isinstance(ar, supported_arrow_array_types):
        return ar.to_pylist()
    else:
        return ar.tolist()


def data_type(ar):
    if isinstance(ar, supported_arrow_array_types):
        return ar.type
    else:
        return ar.dtype


def to_numpy(x, strict=False):
    import vaex.arrow.convert
    import vaex.column
    if isinstance(x, vaex.column.ColumnStringArrow):
        if strict:
            return x.to_numpy()
        else:
            return x.to_arrow()
    elif isinstance(x, np.ndarray):
        return x
    elif isinstance(x, supported_arrow_array_types):
        x = vaex.arrow.convert.column_from_arrow_array(x)
        return to_numpy(x, strict=strict)
    elif hasattr(x, "to_numpy"):
        x = x.to_numpy()
    return np.asanyarray(x)


def to_arrow(x, convert_to_native=True):
    if isinstance(x, supported_arrow_array_types):
        return x
    if convert_to_native and isinstance(x, np.ndarray):
        x = vaex.utils.to_native_array(x)
    return pa.array(x)


def to_xarray(x):
    import xarray
    return xarray.DataArray(to_numpy(x))


def convert(x, type, default_type="numpy"):
    import vaex.column
    if type == "numpy":
        if isinstance(x, (list, tuple)):
            return np.concatenate([convert(k, type) for k in x])
        else:
            return to_numpy(x, strict=True)
    elif type == "arrow":
        if isinstance(x, (list, tuple)):
            return pa.chunked_array([convert(k, type) for k in x])
        else:
            return to_arrow(x)
    elif type == "xarray":
        return to_xarray(x)
    elif type in ['list', 'python']:
        return convert(x, 'numpy').tolist()
    elif type is None:
        if isinstance(x, (list, tuple)):
            chunks = [convert(k, type) for k in x]
            if isinstance(chunks[0], (pa.Array, pa.ChunkedArray, vaex.column.ColumnStringArrow)):
                return convert(chunks, "arrow")
            elif isinstance(chunks[0], np.ndarray):
                return convert(chunks, "numpy")
            else:
                raise ValueError("Unknown type: %r" % chunks[0])
        else:
            # return convert(x, Nonedefault_type)
            return x
    else:
        raise ValueError("Unknown type: %r" % type)


def numpy_dtype(x, strict=False):
    assert not strict
    from . import column
    if isinstance(x, column.ColumnString):
        return x.dtype
    elif isinstance(x, np.ndarray):
        return x.dtype
    elif isinstance(x, supported_arrow_array_types):
        arrow_type = x.type
        if isinstance(arrow_type, pa.DictionaryType):
            # we're interested in the type of the dictionary or the indices?
            if isinstance(x, pa.ChunkedArray):
                # take the first dictionaryu
                x = x.chunks[0]
            return numpy_dtype(x.dictionary)
        if arrow_type in string_types:
            return arrow_type
        dtype = arrow_type.to_pandas_dtype()
        dtype = np.dtype(dtype)  # turn into instance
        return dtype
    else:
        raise TypeError("Cannot determine numpy dtype from: %r" % x)


def arrow_type(x):
    if isinstance(x, supported_arrow_array_types):
        return x.type
    else:
        return to_arrow(x[0:1]).type


def to_arrow_type(data_type):
    if isinstance(data_type, np.dtype):
        return arrow_type_from_numpy_dtype(data_type)
    else:
        return data_type


def to_numpy_type(data_type):
    if isinstance(data_type, np.dtype):
        return data_type
    else:
        return numpy_dtype_from_arrow_type(data_type)


def arrow_type_from_numpy_dtype(dtype):
    data = np.empty(1, dtype=dtype)
    return arrow_type(data)


def numpy_dtype_from_arrow_type(arrow_type):
    data = pa.array([], type=arrow_type)
    return numpy_dtype(data)


def type_promote(t1, t2):
    # when two ndarrays, we keep it like it
    if isinstance(t1, np.dtype) and isinstance(t2, np.dtype):
        return np.promote_types(t1, t2)
    # otherwise we go to arrow
    t1 = to_arrow_type(t1)
    t2 = to_arrow_type(t2)

    if pa.types.is_null(t1):
        return t2
    if pa.types.is_null(t2):
        return t1

    if t1 == t2:
        return t1


    # TODO: so far we only use this in in code that converts to arrow
    # if we want to support numpy, we have to check it types were numpy types
    is_numerics = [pa.types.is_floating, pa.types.is_integer]
    if any(test(t1) for test in is_numerics) and any(test(t2) for test in is_numerics):
        # leverage numpy for type promotion
        dtype1 = numpy_dtype_from_arrow_type(t1)
        dtype2 = numpy_dtype_from_arrow_type(t2)
        dtype = np.promote_types(dtype1, dtype2)
        return arrow_type_from_numpy_dtype(dtype)
    elif is_string_type(t1):
        return t1
    elif is_string_type(t2):
        return t2
    else:
        raise TypeError(f'Cannot promote {t1} and {t2} to a common type')
