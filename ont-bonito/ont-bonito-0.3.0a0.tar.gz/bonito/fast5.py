"""
Bonito Fast5 Utils
"""

import os
import sys
from glob import glob
from functools import partial
from multiprocessing import Pool
from itertools import chain, starmap

import numpy as np
from scipy.signal import find_peaks
from ont_fast5_api.fast5_interface import get_fast5_file


class Read:

    def __init__(self, read, filename):

        self.read_id = read.read_id
        self.run_id = read.get_run_id().decode()
        self.filename = os.path.basename(read.filename)

        read_attrs = read.handle[read.raw_dataset_group_name].attrs
        channel_info = read.handle[read.global_key + 'channel_id'].attrs

        self.offset = int(channel_info['offset'])
        self.sampling_rate = channel_info['sampling_rate']
        self.scaling = channel_info['range'] / channel_info['digitisation']

        self.mux = read_attrs['start_mux']
        self.channel = channel_info['channel_number'].decode()
        self.start = read_attrs['start_time'] / self.sampling_rate
        self.duration = read_attrs['duration'] / self.sampling_rate

        # no trimming
        self.template_start = self.start
        self.template_duration = self.duration

        raw = read.handle[read.raw_dataset_name][:]
        scaled = np.array(self.scaling * (raw + self.offset), dtype=np.float32)

        if len(scaled) > 8000:
            med, mad = med_mad(scaled)
            self.signal = (scaled - med) / mad
        else:
            self.signal = norm_by_noisiest_section(scaled)

    def __repr__(self):
        return "Read('%s')" % self.read_id


def med_mad(x, factor=1.4826):
    """
    Calculate signal median and median absolute deviation
    """
    med = np.median(x)
    mad = np.median(np.absolute(x - med)) * factor
    return med, mad


def norm_by_noisiest_section(signal, samples=100, threshold=6.0):
    """
    Normalise using the medmad from the longest continuous region where the
    noise is above some threshold relative to the std of the full signal.
    """
    threshold = signal.std() / threshold
    noise = np.ones(signal.shape)

    for idx in np.arange(signal.shape[0] // samples):
        window = slice(idx * samples, (idx + 1) * samples)
        noise[window] = np.where(signal[window].std() > threshold, 1, 0)

    # start and end low for peak finding
    noise[0] = 0; noise[-1] = 0
    peaks, info = find_peaks(noise, width=(None, None))

    if len(peaks):
        widest = np.argmax(info['widths'])
        med, mad = med_mad(signal[info['left_bases'][widest]: info['right_bases'][widest]])
    else:
        med, mad = med_mad(signal)
    return (signal - med) / mad


def get_raw_data(filename, read_ids=None, skip=False):
    """
    Get the raw signal and read id from the fast5 files
    """
    with get_fast5_file(filename, 'r') as f5_fh:
        for read_id in f5_fh.get_read_ids():
            if read_ids is None or (read_id in read_ids) ^ skip:
                yield Read(f5_fh.get_read(read_id), filename)


def get_read_ids(filename, read_ids=None, skip=False):
    """
    Get all the read_ids from the file `filename`.
    """
    with get_fast5_file(filename, 'r') as f5_fh:
        ids = [(filename, rid) for rid in f5_fh.get_read_ids()]
        if read_ids is None:
            return ids
        return [rid for rid in ids if (rid[1] in read_ids) ^ skip]


def get_raw_data_for_read(info):
    """
    Get the raw signal from the fast5 file for a given filename, read_id pair
    """
    filename, read_id = info
    with get_fast5_file(filename, 'r') as f5_fh:
        return Read(f5_fh.get_read(read_id), filename)


def get_reads(directory, read_ids=None, skip=False, max_read_size=4e6, n_proc=1):
    """
    Get all reads in a given `directory`.
    """
    get_filtered_reads = partial(get_read_ids, read_ids=read_ids, skip=skip)
    with Pool(n_proc) as pool:
        for job in chain(pool.imap(get_filtered_reads, glob("%s/*.fast5" % directory))):
            for read in pool.imap(get_raw_data_for_read, job):
                if len(read.signal) > max_read_size:
                    sys.stderr.write(
                        "> skipping long read %s (%s samples)\n" % (read.read_id, len(read.signal))
                    )
                    continue
                yield read
