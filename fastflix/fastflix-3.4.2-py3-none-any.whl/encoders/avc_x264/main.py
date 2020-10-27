#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Chris Griffith"
from pathlib import Path

import pkg_resources

name = "AVC (x264)"
requires = "libx264"

video_extension = "mkv"
video_dimension_divisor = 1
icon = str(Path(pkg_resources.resource_filename(__name__, f"../../data/encoders/icon_x264.png")).resolve())

enable_subtitles = True
enable_audio = True
enable_attachments = True

audio_formats = [
    "aac",
    "aac_mf",
    "libfdk_aac",
    "ac3",
    "ac3_fixed",
    "ac3_mf",
    "adpcm_adx",
    "g722",
    "g726",
    "g726le",
    "adpcm_ima_qt",
    "adpcm_ima_ssi",
    "adpcm_ima_wav",
    "adpcm_ms",
    "adpcm_swf",
    "adpcm_yamaha",
    "alac",
    "libopencore_amrnb",
    "libvo_amrwbenc",
    "aptx",
    "aptx_hd",
    "comfortnoise",
    "dca",
    "eac3",
    "flac",
    "g723_1",
    "libgsm",
    "libgsm_ms",
    "libilbc",
    "mlp",
    "mp2",
    "mp2fixed",
    "libtwolame",
    "mp3_mf",
    "libmp3lame",
    "nellymoser",
    "opus",
    "libopus",
    "pcm_alaw",
    "pcm_dvd",
    "pcm_f32be",
    "pcm_f32le",
    "pcm_f64be",
    "pcm_f64le",
    "pcm_mulaw",
    "pcm_s16be",
    "pcm_s16be_planar",
    "pcm_s16le",
    "pcm_s16le_planar",
    "pcm_s24be",
    "pcm_s24daud",
    "pcm_s24le",
    "pcm_s24le_planar",
    "pcm_s32be",
    "pcm_s32le",
    "pcm_s32le_planar",
    "pcm_s64be",
    "pcm_s64le",
    "pcm_s8",
    "pcm_s8_planar",
    "pcm_u16be",
    "pcm_u16le",
    "pcm_u24be",
    "pcm_u24le",
    "pcm_u32be",
    "pcm_u32le",
    "pcm_u8",
    "pcm_vidc",
    "real_144",
    "roq_dpcm",
    "s302m",
    "sbc",
    "sonic",
    "sonicls",
    "libspeex",
    "truehd",
    "tta",
    "vorbis",
    "libvorbis",
    "wavpack",
    "wmav1",
    "wmav2",
]

from fastflix.encoders.avc_x264.command_builder import build
from fastflix.encoders.avc_x264.settings_panel import AVC as settings_panel
