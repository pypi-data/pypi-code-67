# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.8
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_sdbf_class', [dirname(__file__)])
        except ImportError:
            import _sdbf_class
            return _sdbf_class
        if fp is not None:
            try:
                _mod = imp.load_module('_sdbf_class', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _sdbf_class = swig_import_helper()
    del swig_import_helper
else:
    import _sdbf_class
del version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr_nondynamic(self, class_type, name, static=1):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    if (not static):
        return object.__getattr__(self, name)
    else:
        raise AttributeError(name)

def _swig_getattr(self, class_type, name):
    return _swig_getattr_nondynamic(self, class_type, name, 0)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object:
        pass
    _newclass = 0



_sdbf_class.KB_swigconstant(_sdbf_class)
KB = _sdbf_class.KB

def new_intp() -> "int *":
    return _sdbf_class.new_intp()
new_intp = _sdbf_class.new_intp

def copy_intp(value: 'int') -> "int *":
    return _sdbf_class.copy_intp(value)
copy_intp = _sdbf_class.copy_intp

def delete_intp(obj: 'int *') -> "void":
    return _sdbf_class.delete_intp(obj)
delete_intp = _sdbf_class.delete_intp

def intp_assign(obj: 'int *', value: 'int') -> "void":
    return _sdbf_class.intp_assign(obj, value)
intp_assign = _sdbf_class.intp_assign

def intp_value(obj: 'int *') -> "int":
    return _sdbf_class.intp_value(obj)
intp_value = _sdbf_class.intp_value
class sdbf_conf(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, sdbf_conf, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, sdbf_conf, name)
    __repr__ = _swig_repr

    def __init__(self, thread_cnt: 'uint32_t', warnings: 'uint32_t', max_elem_ct: 'uint32_t', max_elem_ct_dd: 'uint32_t'):
        this = _sdbf_class.new_sdbf_conf(thread_cnt, warnings, max_elem_ct, max_elem_ct_dd)
        try:
            self.this.append(this)
        except Exception:
            self.this = this
    __swig_destroy__ = _sdbf_class.delete_sdbf_conf
    __del__ = lambda self: None
sdbf_conf_swigregister = _sdbf_class.sdbf_conf_swigregister
sdbf_conf_swigregister(sdbf_conf)

class sdbf(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, sdbf, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, sdbf, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _sdbf_class.new_sdbf(*args)
        try:
            self.this.append(this)
        except Exception:
            self.this = this
    __swig_destroy__ = _sdbf_class.delete_sdbf
    __del__ = lambda self: None

    def name(self) -> "std::string":
        return _sdbf_class.sdbf_name(self)

    def size(self) -> "uint64_t":
        return _sdbf_class.sdbf_size(self)

    def input_size(self) -> "uint64_t":
        return _sdbf_class.sdbf_input_size(self)

    def compare(self, other: 'sdbf', sample: 'uint32_t') -> "int32_t":
        return _sdbf_class.sdbf_compare(self, other, sample)

    def to_string(self) -> "std::string":
        return _sdbf_class.sdbf_to_string(self)

    def get_index_results(self) -> "std::string":
        return _sdbf_class.sdbf_get_index_results(self)

    def clone_filter(self, position: 'uint32_t') -> "uint8_t *":
        return _sdbf_class.sdbf_clone_filter(self, position)

    def filter_count(self) -> "uint32_t":
        return _sdbf_class.sdbf_filter_count(self)
    __swig_setmethods__["config"] = _sdbf_class.sdbf_config_set
    __swig_getmethods__["config"] = _sdbf_class.sdbf_config_get
    if _newclass:
        config = _swig_property(_sdbf_class.sdbf_config_get, _sdbf_class.sdbf_config_set)
    __swig_getmethods__["get_elem_count"] = lambda x: _sdbf_class.sdbf_get_elem_count
    if _newclass:
        get_elem_count = staticmethod(_sdbf_class.sdbf_get_elem_count)
sdbf_swigregister = _sdbf_class.sdbf_swigregister
sdbf_swigregister(sdbf)
cvar = _sdbf_class.cvar

def sdbf_get_elem_count(mine: 'sdbf', index: 'uint64_t') -> "int32_t":
    return _sdbf_class.sdbf_get_elem_count(mine, index)
sdbf_get_elem_count = _sdbf_class.sdbf_get_elem_count

# This file is compatible with both classic and new-style classes.


