from astropy.io import fits as _fits
from astropy import table as _table
from astropy.time import Time as _Time
from numpy import ma as _ma
import numpy as _np
import scipy.sparse as _sparse
import re as _re 

from .hdu import *
from . import utils as _u
from . import fitsutils as _fu

from .hdu.base import _ValidHDU
from .hdu.table import _OITableHDU
from .hdu.data import _DataHDU
from .hdu.target import _TargetHDU
from .hdu.array import _ArrayHDU
from .hdu.wavelength import _WavelengthHDU
from .hdu.referenced import _Referenced
from .hdu.corr import _CorrHDU
from .hdu.inspol import _InspolHDU
from .hdu.primary import _PrimaryHDU


def open(filename, mode='readonly', lazy_load_hdus=True, **kwargs):
    """

Open an OIFITS file.

Arguments
---------

filename (str)
    File name
mode (str, optional, default: 'readonly')
    Read mode
lazy_load_hdus (bool, optional, default: True)
    Whether to only load HDUs if needed

    """
    # we need to read the primary HDU to see which FITS version it is
    if mode == 'ostream':
        cls = OIFITS2
    else:
        with _fits.open(filename, lazy_load_hdus=True) as hdulist:
            if list.__len__(hdulist): # len(h) would load all HDUs
                content = hdulist[0].header.get('CONTENT', '')
                cls = OIFITS2 if content == 'OIFITS2' else OIFITS1
            else:
                cls = OIFITS2
    hdus = cls.fromfile(filename, lazy_load_hdus=lazy_load_hdus, **kwargs)
    return hdus

def openlist(filenames):
    """

Open a list of OIFITS files and merge them.

Arguments
---------

filenames (str × N)
    File names

    """
    hdulists = [open(f, lazy_load_hdus=False) for f in filenames]
    hdulist = _merge(*hdulists, _inplace=True)

    return hdulist

def merge(*hdulists):
    """

Merge several OIFITS.

Arguments
---------

hdulists1, hdulist2, ...
    OIFITS objects 

    """
    return _merge(*hdulists, _inplace=False)     

def _merge(*hdulists, _inplace=False):


    # Use the latest OIFITS version used by the OIFITS to be merged
    # We order them by newest version first.

    oiver = [getattr(hdulist, '_OI_VER', 0) for hdulist in hdulists]
    order = _np.argsort(oiver)[::-1]
    hdulists = [hdulists[o] for o in order]
    
    
    maxver = oiver[order[0]]
    cls = type(hdulists[order[0]])

    # Copy files if necessary
    if not _inplace:
        hdulists = [hdulist.copy() for hdulist in hdulists]
    
    # Trick to avoid Delayed columns
    # for hdulist in hdulists:
    #    for hdu in hdulist:
    #        nope = hdu.data

    # A flat array containing all HDUs.  They keep knowledge of their
    # container.
    hdus = [hdu for hdulist in hdulists for hdu in hdulist]

    
    # The processing steps:
    # * build a composite header from OIFITS primary headers
    # * convert non-void primary headers into image HDUs
    _process_primaryHDUs(hdus)

    # * remove duplicates (OI tables only)
    _remove_equal_OITableHDUs(hdus)

    # * merge TargetHDU, ArrayHDU when possible
    _merge_OITableHDUs(hdus, cls=(_TargetHDU, _ArrayHDU))

    # * duplicate references ARRNAME, INSNAME, CORRNAME leads
    #   to renaming.  Unfortunately HDUs to be merged will be
    #   needlessly copied here
    _rename_conflicting_OITableHDUs(hdus)

    # * merge interferometric data tables where possible
    _merge_OITableHDUs(hdus, cls=_DataHDU)

    # * if some extensions are of the wrong version, convert them
    for i, hdu in enumerate(hdus):
        if isinstance(hdu, _ValidHDU):
            hdus[i] = hdu.to_version(maxver)
    
    # * update the primary HDU header inferring some keywords from 
    #   contents
    merged = cls(hdus)
    merged.update_primary_header()
    
    # * final tweaks
    merged.verify('silentfix+ignore')
    merged.sort()
    merged.update_extver()

    return merged

def _process_primaryHDUs(hdus):
    
    # merge primary headers of OIFITs primary HDUs 
    headers = [hdu.header for hdu in hdus if isinstance(hdu, _PrimaryHDU)]
    header = _fu.merge_fits_headers(*headers)
    hdus[0].header = header
    # delete void OIFIT Primary headers and convert others to images
    for i in range(len(hdus)-1, 0, -1):
        hdu = hdus[i]
        if isinstance(hdu, _fits.PrimaryHDU):
            if hdu.data is not None:
                hdus[i] = _fits.ImageHDU(hdu)
            else:
                del hdus[i]
       
def _remove_equal_OITableHDUs(hdus, cls=_OITableHDU):
    
    for i, hdu in enumerate(hdus):

        if not isinstance(hdu, cls):
            continue

        for j in range(len(hdus)-1, i, -1):
            if hdus[j] == hdu:
                del hdus[j]     


def _rename_conflicting_OITableHDUs(hdus, cls=_Referenced):

    for i, hdu1 in enumerate(hdus):

        if not isinstance(hdu1, cls):
            continue
            
        refkey = getattr(hdu1, '_REFERENCE_KEY', None)
        if not refkey:
            continue 

        # We then look if any further HDU has a duplicate name of hdus[i]. 
        # Sequential Name behaves like a string 'refname_number' aware
        # of its own numbering.

        hdus2 = hdus[i + 1:]
        
        refname1 = _u.SequentialName(hdu1.header[refkey])
        refhdus2 = [hdu2 for hdu2 in hdus2 if hdu2 & hdu1]
        refnames2 = [_u.SequentialName(h.header[refkey]) for h in refhdus2] 
        equal = [refname1 == refname2 for refname2 in refnames2]
        indices = _np.argwhere(equal)[:,0]
        nequal = len(indices)
        if not nequal:
            continue

        # If there are equal names, then rename using name_number.  We
        # need to look at name_number to pick a non used number...
        # seqname1 % seqname2 means same name but different number.  From
        # the list, we can pick available names. 
     
        refs = [refname2 for refname2 in refnames2 if refname2 % refname1] 
        new_refnames2 = refname1.next_available(refs, nequal)

        for index in indices:

            #refname2 = refnames2[index]
            refhdu2 = refhdus2[index]
            new_refname2 = str(new_refnames2.pop(0))
            refhdu2.rename(new_refname2)

            #container = refhdu2.get_container()
            #if not container:
            #    continue
        
            #referrers = container.get_referrers(refhdu2)
            #for h in referrers:
            #    h.header[refkey] = new_refname2
            #
            #refhdu2.header[refkey] = new_refname2
            #
            #if refkey == 'INSNAME':
            #    for h in container.getInspolHDU():
            #        insname = h.data['INSNAME'] 
            #        h.data['INSNAME'][insname == refname2] = new_refname2


def _merge_OITableHDUs(hdus, cls=_OITableHDU):

    # find all equal HDUs and remove them

    for i, hdu in enumerate(hdus):    

        if not isinstance(hdu, cls):
            continue
        
        # Find all mergeable HDUs, merge them 
        nhdu = len(hdus)
        is_mergeable = [hdus[k] % hdu if k > i else False for k in range(nhdu)]
        where_mergeable = _np.argwhere(is_mergeable)[:,0]
        if len(where_mergeable):
            mergeable = [hdus[m] for m in where_mergeable]
            hdus[i] = hdus[i].merge(*mergeable)
            for j in where_mergeable[::-1]:
                del hdus[j]
   
class _OIFITS(_fits.HDUList):

    _merge_station_distance = 0.1    # 0.1 m
    _merge_array_distance = 10       # 10 m
    _merge_target_distance = 2.5e-8  # ~0.005 mas 
    _merge_target_name_match = False # allow different target designations.


    @staticmethod
    def set_merge_settings(*, station_distance=0.1, array_distance=10, 
           target_distance=2.5e-8, target_name_match=False):
        """

Set the default behaviour when merging several OIFITS objects

Arguments
---------

station_distance (float, default: 0.1)
    Maximum distance (m) for stations to be considered the same
array_distance (float, default: 10)
    Maxiumum distance (m) for array centres to be considered from
    the same array
target_distance (float, default: 2.5e-8 i.e. 5 mas)
    Maximum distance (deg) for two targets to be considered the
    same one
target_name_match (bool, default: False)
    Whether target names must match exactly to be considered the
    same one

        """
        _OIFITS._merge_station_distance = station_distance
        _OIFITS._merge_array_distance = array_distance
        _OIFITS._merge_target_distance = target_distance
        _OIFITS._merge_target_name_match = target_name_match

    def __repr__(self):

        name = type(self).__name__
        str_ = [str(h) for h  in self]
        return f"<{name} at {hex(id(self))}: {' '.join(str_)}>"

    def __str__(self):

        name = type(self).__name__
        str_ = [str(h) for h  in self]

        return f"<{name}: {' '.join(str_)}>"
   
    def __init__(self, hdus=[], file=None):
        super().__init__(hdus=hdus, file=file)  
        for hdu in list.__iter__(hdus):
            hdu._container = self

    # original _read_next_hdu() uses super().append(), ruining any clean 
    # attempt to subclass HDUList
    def _read_next_hdu(self):
        
        has_new_hdu = super()._read_next_hdu()
        if has_new_hdu:
            last_index = list.__len__(self) - 1 # len(x) would load all HDUs
            hdu = self[last_index]
            if isinstance(hdu, _OITableHDU):
                hdu._container = self
        return has_new_hdu

    def get_version(self):
        return self._OI_VER

    def _verify(self, option='warn'):

        errors = super()._verify(option) 
      
        clsname = type(self).__name__
 
        # check OI extensions are valid names and fit the OIFITS version
        for hdu in self[1:]:
            
            extname = hdu.header.get('EXTNAME', '')
            extrevn = hdu.header.get('OI_REVN', 0)
            
            if extname[0:3] == 'OI_' and not isinstance(hdu, _OITableHDU):
                err_text = f"Invalid OIFITS extention: {extname}"
                fix_text = "Replaced underscore by dash"
                def fix(hdu=hdu):
                    hdu.header['EXTNAME'] = 'OI-' + extname[3:]
                err = self.run_option(option, err_text=err_text,
                                  fix_text=fix_text, fix=fix)
                errors.append(err)
              
            if hdu._OI_VER != self._OI_VER: 
                err_text = f"Extension {extname} rev. {extrevn} in {clsname}"
                err = self.run_option(option, err_text=err_text, fixable=False) 
                errors.append(err)
       
        # silently fix EXTVER 
        self.update_extver()
        self.update_primary_header()

        return errors

    def update_uv(self):
        """

Update the (u, v) coordinates (UCOORD, VCOORD) using information of
the array and target information contained in OI_ARRAY and OI_TARGET 
tables.

It is a low-precision routine not meant for high precision work.

Warnings
--------

(u, v) may differ from (UCOORD, VCOORD) determined by a data processing
software because

a. (UCOORD, VCOORD) can be averaged independently from MJD 
(see OIFITS standard)
b. Atmospheric refraction is dealt with approximately, while (UCOORD,
   VCOORD) may have none to full modelling of the atmosphere.

For the VLTI, the difference amount to 0.1-0.2% error on baselines
(a few centimetres).

        """
        for hdu in self.get_dataHDUs():
            hdu.update_uv()

    def get_HDUs(self, exttype, filter=None):
        """
Get all HDUs of a given extension type matching given criteria

Arguments
---------

exttype (type)
    Extension type
filter (func)
    Function taking an extension object and returning either True or 
    False

        """
        hdus = [h for h in self[1:] if isinstance(h, exttype)]
        
        if filter is not None:
            hdus = [h for h in hdus if filter(h)]

        return hdus
    
    def get_dataHDUs(self):
        """
Get all HDUs containing optical interferometry data
        """
        return self.get_HDUs(_DataHDU)

    def get_HDU(self, extype, filter=None):
        """
Get the first HDU of a given extension type matching given criteria

Arguments
---------

exttype (type)
    Extension type
filter (func)
    Function taking an extension object and returning either True or 
    False

        """
        hdus = self.get_HDUs(extype, filter=filter)
        
        if not hdus:
            return None
        return hdus[0]

    def get_OITableHDUs(self):
        """
Get all HDUs containing an OI binary table
        """
        return self.get_HDUs(_OITableHDU)

    def get_arrayHDUs(self):
        return self.get_HDUs(_ArrayHDU)
    
    def get_arrayHDU(self, arrname):
        """
Get HDU containing array description (OI_ARRAY)

Arguments
---------

arrname (str)
    Name of the array

        """
        def same_arrname(h): return h.get_arrname() == arrname
        return self.get_HDU(_ArrayHDU, same_arrname)

    def get_targetHDU(self):
        """
Get the HDU containing target information (OI_TARGET)
        """
        return self.get_HDU(_TargetHDU) 

    def get_wavelengthHDUs(self):
        """
Get all HDUs containing wavelength information (OI_WAVELENGTH)
        """
        return self.get_HDUs(_WavelengthHDU)

    def get_wavelengthHDU(self, insname):
        """
Get the HDU containing wavelength information (OI_WAVELENGTH) of a 
given instrumental setup.

Arguments
---------

insname (str)
    Name of the instrumental setup

        """ 
        def same_insname(h): return h.get_insname() == insname
        return self.get_HDU(_WavelengthHDU, same_insname)

    def get_corrHDUs(self):
        """
Get all HDUs containing correlation information (OI_CORR)
        """
        return self.get_HDUs(_CorrHDU)

    def get_corrHDU(self, corrname):
        """
Get the HDU containing a correlation matrix (OI_CORR)

Arguments
---------

corrname:
    Name of the correlation matrix

        """
        def same_corrname(h): h.get_corrname() == corrname
        return self.get_HDU(_CorrHDU, same_corrname)

    def get_inspolHDU(self, arrname):
        """
Get the HDU containing the instrumental polarisation (OI_INSPOL)
corresponding to a given array.

Arguments
---------

arrname:
    Name of the array

        """
        def same_arrname(h): return h.get_arrname() == arrname
        return self.get_HDU(_InspolHDU, same_arrname)

    def _to_table(self, *, correlations=None, remove_masked=False):

        dataHDUs = self.get_dataHDUs()

        return_corr = correlations is not None

        # join all tables generated by each data HDU
        tabs = [h._to_table(full_uv=True, correlations=return_corr,
                    remove_masked=remove_masked) for h in dataHDUs]
        colnames = tabs[0].colnames 
        cols = [_ma.hstack([t[n] for t in tabs]) for n in colnames]
        tab = _table.Table(cols, names=colnames)
        for name in colnames:
            tab.columns[name].format = tabs[0].columns[name].format

        if not return_corr:
            return tab

        corr = _sparse.identity(len(tab), format='dok') 

        # treat each OI_CORR separately, then look up indices
        # in the full table
        for corrHDU in np.unique(self.get_corrHDUs()):

            corrname = corrHDU.get_corrname()
            keep = tab['CORRNAME'] == corrname
            
            # global index: goes from 0 to len(tab) - 1
            # local index: CORRINDX tabulated for each OI_CORR
            gi = np.argwhere(keep)[:,0]
            li = tab['CORRINDX'][keep]

            xmatch = {l: g for l, g in zip(li, gi) if not li.mask}

            # looks quite pedestrian, can't I vectorise that?
            for line in corrHDU.data:
                i = xmatch[line['IINDX']]
                j = xmatch[line['JINDX']]
                val = line['CORR']
                if val != 0:
                    corr[i,j] = val
                    corr[j,i] = val

        tab.remove_columns(['CORRNAME', 'CORRINDX'])

        if correlations == 'csr':
            corr = corr.tocsr()
        elif correlations == 'csc':
            corr = corr.tocsc()
        elif correlations == 'coo':
            corr = corr.tocoo()
        elif correlations == 'numpy':
            corr = corr.toarray()
        elif correlations == 'matrix':
            corr = corr.todense()
        elif correlations == 'dok':
            pass
        else:
            raise ValueError(f"wrong correlation matrix format: {correlations}")

        return tab, corr

    def append(self, h2):
        """Not implemented"""
        raise NotImplementedError()

    def pop(self, index=-1):
        """Not implemented"""
        raise NotImplementedError()

    def copy(self):
        """

Create a duplicate of an OIFITS, without an attached file, with data 
and header are copied

        """
        return type(self)([h.copy() for h in self])

    def __add__(self, other):
        return merge(self, other)

    def update_extver(self):
        """

Update the EXTVER header keyword in extensions sharing the same name. 
While certainly unused by applications, this is a requirement of the
FITS standard.

        """
        extnames = _np.unique(h.header.get('EXTNAME', None) for h in self[1:])
        for extname in extnames:
            hdus = [h for h in self[1:] 
                            if h.header.get('EXTNAME', None) == extname]
            if len(hdus) > 1:
                for i, h in enumerate(hdus):
                    h.header['EXTVER'] = i + 1

    def to_version(self, n):
        """
Convert an OIFITS object to version 1 or 2 of the standard.

Arguments
---------

n (int: 1 or 2)
    Version of the OIFITS standard

        """
        cls = type(self)
        for newcls in type(self).__base__.__subclasses__():
            if newcls._OI_VER == n:
                break

        hdulist = newcls([hdu.to_version(n) for hdu in self])

        return hdulist 

    def update_primary_header(self):
        """

Update the primary header to match the information in OI table 
extensions

        """ 
        header = self[0].header
        datahdus = self.get_dataHDUs()
        
        # fix dates
        mjdobs = min(h.MJD.min() for h in datahdus)
        header['DATE-OBS'] = _Time(mjdobs, format='mjd').isot 
        
        # deal with keywords for atomic observations
        targets = self.get_targetHDU().data
        if len(targets) == 1:
            wavehdus = self.get_wavelengthHDUs()
            mjdend = max(h.MJD.max() for h in datahdus)
            header['OBJECT'] = targets['TARGET'][0] 
            header['RA'] = targets['RAEP0'][0]
            header['DEC'] = targets['DECEP0'][0]
            header['EQUINOX'] = targets['EQUINOX'][0]
            header['MJD-OBS'] = mjdobs
            header['MJD-END'] = mjdend
            header['WAVELMIN'] = min(h.EFF_WAVE.min() for h in wavehdus)
            header['WAVELMAX'] = max(h.EFF_WAVE.max() for h in wavehdus)
        else:
            for keyw in ['RA', 'DEC', 'UTC', 'LST', 'EQUINOX', 'RADECSYS', 
                'TEXPTIME', 'MJD-OBS', 'MJD-END', 'BASE_MIN', 'BASE_MAX', 
                'WAVELMIN', 'WAVELMAX', 'NUM_CHAN', 'VIS2ERR', 'VISPHERR', 
                'T3PHIERR']:
                if keyw in header:
                    del header[keyw]

        # Deal with all MULTI keywords
        if len(targets) > 1:
            header['OBJECT'] = 'MULTI'

        arrnames = _np.unique([h.get_arrname() for h in datahdus])
        if len(arrnames) == 1:
            header['TELESCOP'] = arrnames[0]
        else:
            header['TELESCOP'] = 'MULTI'

        insnames = _np.unique([h.get_insname() for h in datahdus])
        if len(insnames) == 1:
            header['INSMODE'] = insnames[0]
        else:
            header['INSMODE'] = 'MULTI'

            # deduce instrument
        ins = [_re.sub('([A-Za-z]+).*', '\\1', i).upper() for i in insnames]
        ins = _np.unique(ins)
        if len(ins) == 1:
            ins = ins[0]
        else:
            ins = 'MULTI'
        self[0].header['INSTRUME'] = ins

        # missing ones
        for keyw in ['PROG_ID', 'REFERENC', 'PROCSOFT', 'OBSTECH',
                     'OBSERVER', 'TELESCOP']:
            if keyw not in header:
                header[keyw] = 'UNKNOWN'

class OIFITS1(_OIFITS):
    """Top-level class of Optical Interferometry FITS format, version 1."""
    _OI_VER = 1
    
    def to_table(self, remove_masked=False):
        """

Convert to a flat table containing one scalar interferometric 
observable per line

Arguments
---------

remove_masked (bool, default: False)
    Remove masked values.

Returns
-------

tab (astropy.table.Table)
    A table with one scalar observable per line.

        """
        return self._to_table(remove_masked=remove_masked)


class OIFITS2(_OIFITS):
    """Top-level class of Optical Interferometry FITS format, version 2."""
    _OI_VER = 2
    
    def to_table(self, correlations=None, remove_masked=False):
        """

Convert to a flat table containing one scalar interferometric 
observable per line

Arguments
---------

correlations (bool, default: None)
    Type of correlation matrix
    * None: no matrix is return
    * 'numpy': numpy 2D array
    * 'matrix': numpy matrix
    * 'dok': scipy.sparse matrix in dictionary of keys format
    * 'csc': scipy.sparse matrix in compressed sparse column format
    * 'csr': scipy.sparse matrix in compressed sparse row format
    * 'coo': scipy.sparse matrix in coordinate format

remove_masked (bool, default: False)
    Remove masked values.


Returns
-------

tab (astropy.table.Table)
    A table with one scalar observable per line.

corr (scipy.sparse.dok_matrix, optional)
    Sparse correlation matrix in a dictionary of keys format

        """
        return self._to_table(correlations=correlations, 
                    remove_masked=remove_masked)


set_merge_settings = _OIFITS.set_merge_settings
