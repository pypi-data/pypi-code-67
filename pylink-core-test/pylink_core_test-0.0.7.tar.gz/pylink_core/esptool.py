#!/usr/bin/env python
#
# ESP8266 & ESP32 family ROM Bootloader Utility
# Copyright (C) 2014-2016 Fredrik Ahlberg, Angus Gratton, Espressif Systems (Shanghai) PTE LTD, other contributors as noted.
# https://github.com/espressif/esptool
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import division, print_function

import argparse
import base64
import binascii
import copy
import hashlib
import inspect
import itertools
import io
import os
import shlex
import struct
import sys
import time
import zlib
import string

kprint = print
cdc = None

try:
    import serial
except ImportError:
    kprint("Pyserial is not installed for %s. Check the README for installation instructions." % (sys.executable))
    raise

# check 'serial' is 'pyserial' and not 'serial' https://github.com/espressif/esptool/issues/269
try:
    if "serialization" in serial.__doc__ and "deserialization" in serial.__doc__:
        raise ImportError("""
esptool.py depends on pyserial, but there is a conflict with a currently installed package named 'serial'.

You may be able to work around this by 'pip uninstall serial; pip install pyserial' \
but this may break other installed Python software that depends on 'serial'.

There is no good fix for this right now, apart from configuring virtualenvs. \
See https://github.com/espressif/esptool/issues/269#issuecomment-385298196 for discussion of the underlying issue(s).""")
except TypeError:
    pass  # __doc__ returns None for pyserial

try:
    import serial.tools.list_ports as list_ports
except ImportError:
    kprint("The installed version (%s) of pyserial appears to be too old for esptool.py (Python interpreter %s). "
          "Check the README for installation instructions." % (sys.VERSION, sys.executable))
    raise

__version__ = "3.0-dev"

MAX_UINT32 = 0xffffffff
MAX_UINT24 = 0xffffff

DEFAULT_TIMEOUT = 3                   # timeout for most flash operations
START_FLASH_TIMEOUT = 20              # timeout for starting flash (may perform erase)
CHIP_ERASE_TIMEOUT = 120              # timeout for full chip erase
MAX_TIMEOUT = CHIP_ERASE_TIMEOUT * 2  # longest any command can run
SYNC_TIMEOUT = 0.1                    # timeout for syncing with bootloader
MD5_TIMEOUT_PER_MB = 8                # timeout (per megabyte) for calculating md5sum
ERASE_REGION_TIMEOUT_PER_MB = 30      # timeout (per megabyte) for erasing a region
MEM_END_ROM_TIMEOUT = 0.05            # special short timeout for ESP_MEM_END, as it may never respond
DEFAULT_SERIAL_WRITE_TIMEOUT = 10     # timeout for serial port write
DEFAULT_CONNECT_ATTEMPTS = 7          # default number of times to try connection


def timeout_per_mb(seconds_per_mb, size_bytes):
    """ Scales timeouts which are size-specific """
    result = seconds_per_mb * (size_bytes / 1e6)
    if result < DEFAULT_TIMEOUT:
        return DEFAULT_TIMEOUT
    return result


DETECTED_FLASH_SIZES = {0x12: '256KB', 0x13: '512KB', 0x14: '1MB',
                        0x15: '2MB', 0x16: '4MB', 0x17: '8MB', 0x18: '16MB'}


def check_supported_function(func, check_func):
    """
    Decorator implementation that wraps a check around an ESPLoader
    bootloader function to check if it's supported.

    This is used to capture the multidimensional differences in
    functionality between the ESP8266 & ESP32/32S2 ROM loaders, and the
    software stub that runs on both. Not possible to do this cleanly
    via inheritance alone.
    """
    def inner(*args, **kwargs):
        obj = args[0]
        if check_func(obj):
            return func(*args, **kwargs)
        else:
            raise NotImplementedInROMError(obj, func)
    return inner


def stub_function_only(func):
    """ Attribute for a function only supported in the software stub loader """
    return check_supported_function(func, lambda o: o.IS_STUB)


def stub_and_esp32_function_only(func):
    """ Attribute for a function only supported by software stubs or ESP32/32S2 ROM """
    return check_supported_function(func, lambda o: o.IS_STUB or isinstance(o, ESP32ROM))


PYTHON2 = sys.version_info[0] < 3  # True if on pre-Python 3

# Function to return nth byte of a bitstring
# Different behaviour on Python 2 vs 3
if PYTHON2:
    def byte(bitstr, index):
        return ord(bitstr[index])
else:
    def byte(bitstr, index):
        return bitstr[index]

# Provide a 'basestring' class on Python 3
try:
    basestring
except NameError:
    basestring = str


def kprint_overwrite(message, last_line=False):
    """ kprint a message, overwriting the currently kprinted line.

    If last_line is False, don't append a newline at the end (expecting another subsequent call will overwrite this one.)

    After a sequence of calls with last_line=False, call once with last_line=True.

    If output is not a TTY (for example redirected a pipe), no overwriting happens and this function is the same as kprint().
    """
    kprint("\r%s" % message, end='\n' if last_line else '')


def _mask_to_shift(mask):
    """ Return the index of the least significant bit in the mask """
    shift = 0
    while mask & 0x1 == 0:
        shift += 1
        mask >>= 1
    return shift


def esp8266_function_only(func):
    """ Attribute for a function only supported on ESP8266 """
    return check_supported_function(func, lambda o: o.CHIP_NAME == "ESP8266")


class ESPLoader(object):
    """ Base class providing access to ESP ROM & software stub bootloaders.
    Subclasses provide ESP8266 & ESP32 specific functionality.

    Don't instantiate this base class directly, either instantiate a subclass or
    call ESPLoader.detect_chip() which will interrogate the chip and return the
    appropriate subclass instance.

    """
    CHIP_NAME = "Espressif device"
    IS_STUB = False

    DEFAULT_PORT = "/dev/ttyUSB0"

    # Commands supported by ESP8266 ROM bootloader
    ESP_FLASH_BEGIN = 0x02
    ESP_FLASH_DATA  = 0x03
    ESP_FLASH_END   = 0x04
    ESP_MEM_BEGIN   = 0x05
    ESP_MEM_END     = 0x06
    ESP_MEM_DATA    = 0x07
    ESP_SYNC        = 0x08
    ESP_WRITE_REG   = 0x09
    ESP_READ_REG    = 0x0a

    # Some comands supported by ESP32 ROM bootloader (or -8266 w/ stub)
    ESP_SPI_SET_PARAMS = 0x0B
    ESP_SPI_ATTACH     = 0x0D
    ESP_READ_FLASH_SLOW  = 0x0e  # ROM only, much slower than the stub flash read
    ESP_CHANGE_BAUDRATE = 0x0F
    ESP_FLASH_DEFL_BEGIN = 0x10
    ESP_FLASH_DEFL_DATA  = 0x11
    ESP_FLASH_DEFL_END   = 0x12
    ESP_SPI_FLASH_MD5    = 0x13

    # Commands supported by ESP32-S2 ROM bootloader only
    ESP_GET_SECURITY_INFO = 0x14

    # Some commands supported by stub only
    ESP_ERASE_FLASH = 0xD0
    ESP_ERASE_REGION = 0xD1
    ESP_READ_FLASH = 0xD2
    ESP_RUN_USER_CODE = 0xD3

    # Flash encryption encrypted data command
    ESP_FLASH_ENCRYPT_DATA = 0xD4

    # Response code(s) sent by ROM
    ROM_INVALID_RECV_MSG = 0x05   # response if an invalid message is received

    # Maximum block sized for RAM and Flash writes, respectively.
    ESP_RAM_BLOCK   = 0x1800

    FLASH_WRITE_SIZE = 0x400

    # Default baudrate. The ROM auto-bauds, so we can use more or less whatever we want.
    ESP_ROM_BAUD    = 115200

    # First byte of the application image
    ESP_IMAGE_MAGIC = 0xe9

    # Initial state for the checksum routine
    ESP_CHECKSUM_MAGIC = 0xef

    # Flash sector size, minimum unit of erase.
    FLASH_SECTOR_SIZE = 0x1000

    UART_DATE_REG_ADDR = 0x60000078  # used to differentiate ESP8266 vs ESP32*
    UART_DATE_REG2_ADDR = 0x3f400074  # used to differentiate ESP32-S2 vs other models

    UART_CLKDIV_MASK = 0xFFFFF

    # Memory addresses
    IROM_MAP_START = 0x40200000
    IROM_MAP_END = 0x40300000

    # The number of bytes in the UART response that signify command status
    STATUS_BYTES_LENGTH = 2

    def __init__(self, port=DEFAULT_PORT, baud=ESP_ROM_BAUD, trace_enabled=False):
        """Base constructor for ESPLoader bootloader interaction

        Don't call this constructor, either instantiate ESP8266ROM
        or ESP32ROM, or use ESPLoader.detect_chip().

        This base class has all of the instance methods for bootloader
        functionality supported across various chips & stub
        loaders. Subclasses replace the functions they don't support
        with ones which throw NotImplementedInROMError().

        """
        
        if cdc:
            self._port = cdc
            kprint("Use cdc over serial")
        elif isinstance(port, basestring):
            self._port = serial.serial_for_url(port)
        else:
            self._port = port
        self._slip_reader = slip_reader(self._port, self.trace)
        # setting baud rate in a separate step is a workaround for
        # CH341 driver on some Linux versions (this opens at 9600 then
        # sets), shouldn't matter for other platforms/drivers. See
        # https://github.com/espressif/esptool/issues/44#issuecomment-107094446
        self._set_port_baudrate(baud)
        self._trace_enabled = trace_enabled
        # set write timeout, to prevent esptool blocked at write forever.
        try:
            self._port.write_timeout = DEFAULT_SERIAL_WRITE_TIMEOUT
        except NotImplementedError:
            # no write timeout for RFC2217 ports
            # need to set the property back to None or it will continue to fail
            self._port.write_timeout = None

    def _set_port_baudrate(self, baud):
        try:
            self._port.baudrate = baud
        except IOError:
            raise FatalError("Failed to set baud rate %d. The driver may not support this rate." % baud)

    @staticmethod
    def detect_chip(port=DEFAULT_PORT, baud=ESP_ROM_BAUD, connect_mode='default_reset', trace_enabled=False,
                    connect_attempts=DEFAULT_CONNECT_ATTEMPTS):
        """ Use serial access to detect the chip type.

        We use the UART's datecode register for this, it's mapped at
        the same address on ESP8266 & ESP32 so we can use one
        memory read and compare to the datecode register for each chip
        type.

        This routine automatically performs ESPLoader.connect() (passing
        connect_mode parameter) as part of querying the chip.
        """
        detect_port = ESPLoader(port, baud, trace_enabled=trace_enabled)
        detect_port.connect(connect_mode, connect_attempts, detecting=True)
        try:
            kprint('Detecting chip type...', end='')
            
            date_reg = detect_port.read_reg(ESPLoader.UART_DATE_REG_ADDR)
            date_reg2 = detect_port.read_reg(ESPLoader.UART_DATE_REG2_ADDR)

            for cls in [ESP8266ROM, ESP32ROM, ESP32S2ROM]:
                if date_reg == cls.DATE_REG_VALUE and (cls.DATE_REG2_VALUE is None or date_reg2 == cls.DATE_REG2_VALUE):
                    # don't connect a second time
                    inst = cls(detect_port._port, baud, trace_enabled=trace_enabled)
                    kprint(' %s' % inst.CHIP_NAME, end='')
                    return inst
        finally:
            kprint('')  # end line
        raise FatalError("Unexpected UART datecode value 0x%08x. Failed to autodetect chip type." % (date_reg))

    """ Read a SLIP packet from the serial port """
    def read(self):
        return next(self._slip_reader)

    """ Write bytes to the serial port while performing SLIP escaping """
    def write(self, packet):
        buf = b'\xc0' \
              + (packet.replace(b'\xdb',b'\xdb\xdd').replace(b'\xc0',b'\xdb\xdc')) \
              + b'\xc0'
        self.trace("Write %d bytes: %s", len(buf), HexFormatter(buf))
        self._port.write(buf)

    def trace(self, message, *format_args):
        if self._trace_enabled:
            now = time.time()
            try:

                delta = now - self._last_trace
            except AttributeError:
                delta = 0.0
            self._last_trace = now
            prefix = "TRACE +%.3f " % delta
            kprint(prefix + (message % format_args))

    """ Calculate checksum of a blob, as it is defined by the ROM """
    @staticmethod
    def checksum(data, state=ESP_CHECKSUM_MAGIC):
        for b in data:
            if type(b) is int:  # python 2/3 compat
                state ^= b
            else:
                state ^= ord(b)

        return state

    """ Send a request and read the response """
    def command(self, op=None, data=b"", chk=0, wait_response=True, timeout=DEFAULT_TIMEOUT):
        saved_timeout = self._port.timeout
        new_timeout = min(timeout, MAX_TIMEOUT)
        if new_timeout != saved_timeout:
            self._port.timeout = new_timeout

        try:
            if op is not None:
                self.trace("command op=0x%02x data len=%s wait_response=%d timeout=%.3f data=%s",
                           op, len(data), 1 if wait_response else 0, timeout, HexFormatter(data))
                pkt = struct.pack(b'<BBHI', 0x00, op, len(data), chk) + data
                self.write(pkt)

            if not wait_response:
                return

            # tries to get a response until that response has the
            # same operation as the request or a retries limit has
            # exceeded. This is needed for some esp8266s that
            # reply with more sync responses than expected.
            for retry in range(100):
                p = self.read()
                if len(p) < 8:
                    continue
                (resp, op_ret, len_ret, val) = struct.unpack('<BBHI', p[:8])
                if resp != 1:
                    continue
                data = p[8:]

                if op is None or op_ret == op:
                    return val, data
                if byte(data, 0) != 0 and byte(data, 1) == self.ROM_INVALID_RECV_MSG:
                    raise UnsupportedCommandError()

        finally:
            if new_timeout != saved_timeout:
                self._port.timeout = saved_timeout

        raise FatalError("Response doesn't match request")

    def check_command(self, op_description, op=None, data=b'', chk=0, timeout=DEFAULT_TIMEOUT):
        """
        Execute a command with 'command', check the result code and throw an appropriate
        FatalError if it fails.

        Returns the "result" of a successful command.
        """
        val, data = self.command(op, data, chk, timeout=timeout)

        # things are a bit weird here, bear with us

        # the status bytes are the last 2/4 bytes in the data (depending on chip)
        if len(data) < self.STATUS_BYTES_LENGTH:
            raise FatalError("Failed to %s. Only got %d byte status response." % (op_description, len(data)))
        status_bytes = data[-self.STATUS_BYTES_LENGTH:]
        # we only care if the first one is non-zero. If it is, the second byte is a reason.
        if byte(status_bytes, 0) != 0:
            raise FatalError.WithResult('Failed to %s' % op_description, status_bytes)

        # if we had more data than just the status bytes, return it as the result
        # (this is used by the md5sum command, maybe other commands?)
        if len(data) > self.STATUS_BYTES_LENGTH:
            return data[:-self.STATUS_BYTES_LENGTH]
        else:  # otherwise, just return the 'val' field which comes from the reply header (this is used by read_reg)
            return val

    def flush_input(self):
        self._port.flushInput()
        self._slip_reader = slip_reader(self._port, self.trace)

    def sync(self):
        self.command(self.ESP_SYNC, b'\x07\x07\x12\x20' + 32 * b'\x55',
                     timeout=SYNC_TIMEOUT)
        for i in range(7):
            self.command()

    def _setDTR(self, state):
        self._port.setDTR(state)

    def _setRTS(self, state):
        self._port.setRTS(state)
        # Work-around for adapters on Windows using the usbser.sys driver:
        # generate a dummy change to DTR so that the set-control-line-state
        # request is sent with the updated RTS state and the same DTR state
        self._port.setDTR(self._port.dtr)

    def _connect_attempt(self, mode='default_reset', esp32r0_delay=False):
        """ A single connection attempt, with esp32r0 workaround options """
        # esp32r0_delay is a workaround for bugs with the most common auto reset
        # circuit and Windows, if the EN pin on the dev board does not have
        # enough capacitance.
        #
        # Newer dev boards shouldn't have this problem (higher value capacitor
        # on the EN pin), and ESP32 revision 1 can't use this workaround as it
        # relies on a silicon bug.
        #
        # Details: https://github.com/espressif/esptool/issues/136
        last_error = None

        # If we're doing no_sync, we're likely communicating as a pass through
        # with an intermediate device to the ESP32
        if mode == "no_reset_no_sync":
            return last_error

        # issue reset-to-bootloader:
        # RTS = either CH_PD/EN or nRESET (both active low = chip in reset
        # DTR = GPIO0 (active low = boot to flasher)
        #
        # DTR & RTS are active low signals,
        # ie True = pin @ 0V, False = pin @ VCC.
        if mode != 'no_reset':
            self._setDTR(False)  # IO0=HIGH
            self._setRTS(True)   # EN=LOW, chip in reset
            time.sleep(0.1)
            if esp32r0_delay:
                # Some chips are more likely to trigger the esp32r0
                # watchdog reset silicon bug if they're held with EN=LOW
                # for a longer period
                time.sleep(1.2)
            self._setDTR(True)   # IO0=LOW
            self._setRTS(False)  # EN=HIGH, chip out of reset
            if esp32r0_delay:
                # Sleep longer after reset.
                # This workaround only works on revision 0 ESP32 chips,
                # it exploits a silicon bug spurious watchdog reset.
                time.sleep(0.4)  # allow watchdog reset to occur
            time.sleep(0.05)
            self._setDTR(False)  # IO0=HIGH, done

        for _ in range(5):
            try:
                self.flush_input()
                self._port.flushOutput()
                self.sync()
                return None
            except FatalError as e:
                if esp32r0_delay:
                    kprint('_', end='')
                else:
                    kprint('.', end='')
                
                time.sleep(0.05)
                last_error = e
        return last_error

    def connect(self, mode='default_reset', attempts=DEFAULT_CONNECT_ATTEMPTS, detecting=False):
        """ Try connecting repeatedly until successful, or giving up """
        kprint('Connecting...', end='')
        
        last_error = None

        try:
            for _ in range(attempts) if attempts > 0 else itertools.count():
                last_error = self._connect_attempt(mode=mode, esp32r0_delay=False)
                if last_error is None:
                    break
                last_error = self._connect_attempt(mode=mode, esp32r0_delay=True)
                if last_error is None:
                    break
        finally:
            kprint('')  # end 'Connecting...' line

        if last_error is not None:
            raise FatalError('Failed to connect to %s: %s' % (self.CHIP_NAME, last_error))

        if not detecting:
            # check the date code registers match what we expect to see
            date_reg = self.read_reg(self.UART_DATE_REG_ADDR)
            date_reg2 = self.read_reg(self.UART_DATE_REG2_ADDR)
            if date_reg != self.DATE_REG_VALUE or (self.DATE_REG2_VALUE is not None and date_reg2 != self.DATE_REG2_VALUE):
                actually = None
                for cls in [ESP8266ROM, ESP32ROM, ESP32S2ROM]:
                    if date_reg == cls.DATE_REG_VALUE and (cls.DATE_REG2_VALUE is None or date_reg2 == cls.DATE_REG2_VALUE):
                        actually = cls
                        break
                if actually is None:
                    kprint(("WARNING: This chip doesn't appear to be a %s (date codes 0x%08x:0x%08x). " +
                          "Probably it is unsupported by this version of esptool.") % (self.CHIP_NAME, date_reg, date_reg2))
                else:
                    raise FatalError("This chip is %s not %s. Wrong --chip argument?" % (actually.CHIP_NAME, self.CHIP_NAME))

    def read_reg(self, addr):
        """ Read memory address in target """
        # we don't call check_command here because read_reg() function is called
        # when detecting chip type, and the way we check for success (STATUS_BYTES_LENGTH) is different
        # for different chip types (!)
        val, data = self.command(self.ESP_READ_REG, struct.pack('<I', addr))
        if byte(data, 0) != 0:
            raise FatalError.WithResult("Failed to read register address %08x" % addr, data)
        return val

    """ Write to memory address in target """
    def write_reg(self, addr, value, mask=0xFFFFFFFF, delay_us=0, delay_after_us=0):
        command = struct.pack('<IIII', addr, value, mask, delay_us)
        if delay_after_us > 0:
            # add a dummy write to a date register as an excuse to have a delay
            command += struct.pack('<IIII', self.UART_DATE_REG_ADDR, 0, 0, delay_after_us)

        return self.check_command("write target memory", self.ESP_WRITE_REG, command)

    def update_reg(self, addr, mask, new_val):
        """ Update register at 'addr', replace the bits masked out by 'mask'
        with new_val. new_val is shifted left to match the LSB of 'mask'

        Returns just-written value of register.
        """
        shift = _mask_to_shift(mask)
        val = self.read_reg(addr)
        val &= ~mask
        val |= (new_val << shift) & mask
        self.write_reg(addr, val)

        return val

    """ Start downloading an application image to RAM """
    def mem_begin(self, size, blocks, blocksize, offset):
        if self.IS_STUB:  # check we're not going to overwrite a running stub with this data
            stub = self.STUB_CODE
            load_start = offset
            load_end = offset + size
            for (start, end) in [(stub["data_start"], stub["data_start"] + len(stub["data"])),
                                 (stub["text_start"], stub["text_start"] + len(stub["text"]))]:
                if load_start < end and load_end > start:
                    raise FatalError(("Software loader is resident at 0x%08x-0x%08x. " +
                                      "Can't load binary at overlapping address range 0x%08x-0x%08x. " +
                                      "Either change binary loading address, or use the --no-stub " +
                                      "option to disable the software loader.") % (start, end, load_start, load_end))

        return self.check_command("enter RAM download mode", self.ESP_MEM_BEGIN,
                                  struct.pack('<IIII', size, blocks, blocksize, offset))

    """ Send a block of an image to RAM """
    def mem_block(self, data, seq):
        return self.check_command("write to target RAM", self.ESP_MEM_DATA,
                                  struct.pack('<IIII', len(data), seq, 0, 0) + data,
                                  self.checksum(data))

    """ Leave download mode and run the application """
    def mem_finish(self, entrypoint=0):
        # Sending ESP_MEM_END usually sends a correct response back, however sometimes
        # (with ROM loader) the executed code may reset the UART or change the baud rate
        # before the transmit FIFO is empty. So in these cases we set a short timeout and
        # ignore errors.
        timeout = DEFAULT_TIMEOUT if self.IS_STUB else MEM_END_ROM_TIMEOUT
        data = struct.pack('<II', int(entrypoint == 0), entrypoint)
        try:
            return self.check_command("leave RAM download mode", self.ESP_MEM_END,
                                      data=data, timeout=timeout)
        except FatalError:
            if self.IS_STUB:
                raise
            pass

    """ Start downloading to Flash (performs an erase)

    Returns number of blocks (of size self.FLASH_WRITE_SIZE) to write.
    """
    def flash_begin(self, size, offset):
        num_blocks = (size + self.FLASH_WRITE_SIZE - 1) // self.FLASH_WRITE_SIZE
        erase_size = self.get_erase_size(offset, size)

        t = time.time()
        if self.IS_STUB:
            timeout = DEFAULT_TIMEOUT
        else:
            timeout = timeout_per_mb(ERASE_REGION_TIMEOUT_PER_MB, size)  # ROM performs the erase up front

        params = struct.pack('<IIII', erase_size, num_blocks, self.FLASH_WRITE_SIZE, offset)
        if isinstance(self, ESP32S2ROM) and not self.IS_STUB:
            params += struct.pack('<I', 0)  # enter encrypted flash mode (ROM version of this is unsupported for now)
        self.check_command("enter Flash download mode", self.ESP_FLASH_BEGIN,
                           params, timeout=timeout)
        if size != 0 and not self.IS_STUB:
            kprint("Took %.2fs to erase flash block" % (time.time() - t))
        return num_blocks

    """ Write block to flash """
    def flash_block(self, data, seq, timeout=DEFAULT_TIMEOUT):
        self.check_command("write to target Flash after seq %d" % seq,
                           self.ESP_FLASH_DATA,
                           struct.pack('<IIII', len(data), seq, 0, 0) + data,
                           self.checksum(data),
                           timeout=timeout)

    """ Encrypt before writing to flash """
    def flash_encrypt_block(self, data, seq, timeout=DEFAULT_TIMEOUT):
        self.check_command("Write encrypted to target Flash after seq %d" % seq,
                           self.ESP_FLASH_ENCRYPT_DATA,
                           struct.pack('<IIII', len(data), seq, 0, 0) + data,
                           self.checksum(data),
                           timeout=timeout)

    """ Leave flash mode and run/reboot """
    def flash_finish(self, reboot=False):
        pkt = struct.pack('<I', int(not reboot))
        # stub sends a reply to this command
        self.check_command("leave Flash mode", self.ESP_FLASH_END, pkt)

    """ Run application code in flash """
    def run(self, reboot=False):
        # Fake flash begin immediately followed by flash end
        self.flash_begin(0, 0)
        self.flash_finish(reboot)

    """ Read SPI flash manufacturer and device id """
    def flash_id(self):
        SPIFLASH_RDID = 0x9F
        return self.run_spiflash_command(SPIFLASH_RDID, b"", 24)

    def get_security_info(self):
        # TODO: this only works on the ESP32S2 ROM code loader and needs to work in stub loader also
        res = self.check_command('get security info', self.ESP_GET_SECURITY_INFO, b'')
        res = struct.unpack("<IBBBBBBBB", res)
        flags, flash_crypt_cnt, key_purposes = res[0], res[1], res[2:]
        # TODO: pack this as some kind of better data type
        return (flags, flash_crypt_cnt, key_purposes)

    def parse_flash_size_arg(self, arg):
        try:
            return self.FLASH_SIZES[arg]
        except KeyError:
            raise FatalError("Flash size '%s' is not supported by this chip type. Supported sizes: %s"
                             % (arg, ", ".join(self.FLASH_SIZES.keys())))

    def run_stub(self, stub=None):
        if stub is None:
            if self.IS_STUB:
                raise FatalError("Not possible for a stub to load another stub (memory likely to overlap.)")
            stub = self.STUB_CODE

        # Upload
        kprint("Uploading stub...")
        for field in ['text', 'data']:
            if field in stub:
                offs = stub[field + "_start"]
                length = len(stub[field])
                blocks = (length + self.ESP_RAM_BLOCK - 1) // self.ESP_RAM_BLOCK
                self.mem_begin(length, blocks, self.ESP_RAM_BLOCK, offs)
                for seq in range(blocks):
                    from_offs = seq * self.ESP_RAM_BLOCK
                    to_offs = from_offs + self.ESP_RAM_BLOCK
                    self.mem_block(stub[field][from_offs:to_offs], seq)
        kprint("Running stub...")
        self.mem_finish(stub['entry'])

        p = self.read()
        if p != b'OHAI':
            raise FatalError("Failed to start stub. Unexpected response: %s" % p)
        kprint("Stub running...")
        return self.STUB_CLASS(self)

    @stub_and_esp32_function_only
    def flash_defl_begin(self, size, compsize, offset):
        """ Start downloading compressed data to Flash (performs an erase)

        Returns number of blocks (size self.FLASH_WRITE_SIZE) to write.
        """
        num_blocks = (compsize + self.FLASH_WRITE_SIZE - 1) // self.FLASH_WRITE_SIZE
        erase_blocks = (size + self.FLASH_WRITE_SIZE - 1) // self.FLASH_WRITE_SIZE

        t = time.time()
        if self.IS_STUB:
            write_size = size  # stub expects number of bytes here, manages erasing internally
            timeout = DEFAULT_TIMEOUT
        else:
            write_size = erase_blocks * self.FLASH_WRITE_SIZE  # ROM expects rounded up to erase block size
            timeout = timeout_per_mb(ERASE_REGION_TIMEOUT_PER_MB, write_size)  # ROM performs the erase up front
        kprint("Compressed %d bytes to %d..." % (size, compsize))
        params = struct.pack('<IIII', write_size, num_blocks, self.FLASH_WRITE_SIZE, offset)
        if isinstance(self, ESP32S2ROM) and not self.IS_STUB:
            params += struct.pack('<I', 0)  # extra param is to enter encrypted flash mode via ROM (not supported currently)
        self.check_command("enter compressed flash mode", self.ESP_FLASH_DEFL_BEGIN, params, timeout=timeout)
        if size != 0 and not self.IS_STUB:
            # (stub erases as it writes, but ROM loaders erase on begin)
            kprint("Took %.2fs to erase flash block" % (time.time() - t))
        return num_blocks

    """ Write block to flash, send compressed """
    @stub_and_esp32_function_only
    def flash_defl_block(self, data, seq, timeout=DEFAULT_TIMEOUT):
        self.check_command("write compressed data to flash after seq %d" % seq,
                           self.ESP_FLASH_DEFL_DATA, struct.pack('<IIII', len(data), seq, 0, 0) + data, self.checksum(data), timeout=timeout)

    """ Leave compressed flash mode and run/reboot """
    @stub_and_esp32_function_only
    def flash_defl_finish(self, reboot=False):
        if not reboot and not self.IS_STUB:
            # skip sending flash_finish to ROM loader, as this
            # exits the bootloader. Stub doesn't do this.
            return
        pkt = struct.pack('<I', int(not reboot))
        self.check_command("leave compressed flash mode", self.ESP_FLASH_DEFL_END, pkt)
        self.in_bootloader = False

    @stub_and_esp32_function_only
    def flash_md5sum(self, addr, size):
        # the MD5 command returns additional bytes in the standard
        # command reply slot
        timeout = timeout_per_mb(MD5_TIMEOUT_PER_MB, size)
        res = self.check_command('calculate md5sum', self.ESP_SPI_FLASH_MD5, struct.pack('<IIII', addr, size, 0, 0),
                                 timeout=timeout)

        if len(res) == 32:
            return res.decode("utf-8")  # already hex formatted
        elif len(res) == 16:
            return hexify(res).lower()
        else:
            raise FatalError("MD5Sum command returned unexpected result: %r" % res)

    @stub_and_esp32_function_only
    def change_baud(self, baud):
        kprint("Changing baud rate to %d" % baud)
        # stub takes the new baud rate and the old one
        second_arg = self._port.baudrate if self.IS_STUB else 0
        self.command(self.ESP_CHANGE_BAUDRATE, struct.pack('<II', baud, second_arg))
        kprint("Changed.")
        self._set_port_baudrate(baud)
        time.sleep(0.05)  # get rid of crap sent during baud rate change
        self.flush_input()

    @stub_function_only
    def erase_flash(self):
        # depending on flash chip model the erase may take this long (maybe longer!)
        self.check_command("erase flash", self.ESP_ERASE_FLASH,
                           timeout=CHIP_ERASE_TIMEOUT)

    @stub_function_only
    def erase_region(self, offset, size):
        if offset % self.FLASH_SECTOR_SIZE != 0:
            raise FatalError("Offset to erase from must be a multiple of 4096")
        if size % self.FLASH_SECTOR_SIZE != 0:
            raise FatalError("Size of data to erase must be a multiple of 4096")
        timeout = timeout_per_mb(ERASE_REGION_TIMEOUT_PER_MB, size)
        self.check_command("erase region", self.ESP_ERASE_REGION, struct.pack('<II', offset, size), timeout=timeout)

    def read_flash_slow(self, offset, length, progress_fn):
        raise NotImplementedInROMError(self, self.read_flash_slow)

    def read_flash(self, offset, length, progress_fn=None):
        if not self.IS_STUB:
            return self.read_flash_slow(offset, length, progress_fn)  # ROM-only routine

        # issue a standard bootloader command to trigger the read
        self.check_command("read flash", self.ESP_READ_FLASH,
                           struct.pack('<IIII',
                                       offset,
                                       length,
                                       self.FLASH_SECTOR_SIZE,
                                       64))
        # now we expect (length // block_size) SLIP frames with the data
        data = b''
        while len(data) < length:
            p = self.read()
            data += p
            if len(data) < length and len(p) < self.FLASH_SECTOR_SIZE:
                raise FatalError('Corrupt data, expected 0x%x bytes but received 0x%x bytes' % (self.FLASH_SECTOR_SIZE, len(p)))
            self.write(struct.pack('<I', len(data)))
            if progress_fn and (len(data) % 1024 == 0 or len(data) == length):
                progress_fn(len(data), length)
        if progress_fn:
            progress_fn(len(data), length)
        if len(data) > length:
            raise FatalError('Read more than expected')

        digest_frame = self.read()
        if len(digest_frame) != 16:
            raise FatalError('Expected digest, got: %s' % hexify(digest_frame))
        expected_digest = hexify(digest_frame).upper()
        digest = hashlib.md5(data).hexdigest().upper()
        if digest != expected_digest:
            raise FatalError('Digest mismatch: expected %s, got %s' % (expected_digest, digest))
        return data

    def flash_spi_attach(self, hspi_arg):
        """Send SPI attach command to enable the SPI flash pins

        ESP8266 ROM does this when you send flash_begin, ESP32 ROM
        has it as a SPI command.
        """
        # last 3 bytes in ESP_SPI_ATTACH argument are reserved values
        arg = struct.pack('<I', hspi_arg)
        if not self.IS_STUB:
            # ESP32 ROM loader takes additional 'is legacy' arg, which is not
            # currently supported in the stub loader or esptool.py (as it's not usually needed.)
            is_legacy = 0
            arg += struct.pack('BBBB', is_legacy, 0, 0, 0)
        self.check_command("configure SPI flash pins", ESP32ROM.ESP_SPI_ATTACH, arg)

    def flash_set_parameters(self, size):
        """Tell the ESP bootloader the parameters of the chip

        Corresponds to the "flashchip" data structure that the ROM
        has in RAM.

        'size' is in bytes.

        All other flash parameters are currently hardcoded (on ESP8266
        these are mostly ignored by ROM code, on ESP32 I'm not sure.)
        """
        fl_id = 0
        total_size = size
        block_size = 64 * 1024
        sector_size = 4 * 1024
        page_size = 256
        status_mask = 0xffff
        self.check_command("set SPI params", ESP32ROM.ESP_SPI_SET_PARAMS,
                           struct.pack('<IIIIII', fl_id, total_size, block_size, sector_size, page_size, status_mask))

    def run_spiflash_command(self, spiflash_command, data=b"", read_bits=0):
        """Run an arbitrary SPI flash command.

        This function uses the "USR_COMMAND" functionality in the ESP
        SPI hardware, rather than the precanned commands supported by
        hardware. So the value of spiflash_command is an actual command
        byte, sent over the wire.

        After writing command byte, writes 'data' to MOSI and then
        reads back 'read_bits' of reply on MISO. Result is a number.
        """

        # SPI_USR register flags
        SPI_USR_COMMAND = (1 << 31)
        SPI_USR_MISO    = (1 << 28)
        SPI_USR_MOSI    = (1 << 27)

        # SPI registers, base address differs ESP32* vs 8266
        base = self.SPI_REG_BASE
        SPI_CMD_REG       = base + 0x00
        SPI_USR_REG       = base + self.SPI_USR_OFFS
        SPI_USR1_REG      = base + self.SPI_USR1_OFFS
        SPI_USR2_REG      = base + self.SPI_USR2_OFFS
        SPI_W0_REG        = base + self.SPI_W0_OFFS

        # following two registers are ESP32 & 32S2 only
        if self.SPI_MOSI_DLEN_OFFS is not None:
            # ESP32/32S2 has a more sophisticated way to set up "user" commands
            def set_data_lengths(mosi_bits, miso_bits):
                SPI_MOSI_DLEN_REG = base + self.SPI_MOSI_DLEN_OFFS
                SPI_MISO_DLEN_REG = base + self.SPI_MISO_DLEN_OFFS
                if mosi_bits > 0:
                    self.write_reg(SPI_MOSI_DLEN_REG, mosi_bits - 1)
                if miso_bits > 0:
                    self.write_reg(SPI_MISO_DLEN_REG, miso_bits - 1)
        else:

            def set_data_lengths(mosi_bits, miso_bits):
                SPI_DATA_LEN_REG = SPI_USR1_REG
                SPI_MOSI_BITLEN_S = 17
                SPI_MISO_BITLEN_S = 8
                mosi_mask = 0 if (mosi_bits == 0) else (mosi_bits - 1)
                miso_mask = 0 if (miso_bits == 0) else (miso_bits - 1)
                self.write_reg(SPI_DATA_LEN_REG,
                               (miso_mask << SPI_MISO_BITLEN_S) | (
                                   mosi_mask << SPI_MOSI_BITLEN_S))

        # SPI peripheral "command" bitmasks for SPI_CMD_REG
        SPI_CMD_USR  = (1 << 18)

        # shift values
        SPI_USR2_COMMAND_LEN_SHIFT = 28

        if read_bits > 32:
            raise FatalError("Reading more than 32 bits back from a SPI flash operation is unsupported")
        if len(data) > 64:
            raise FatalError("Writing more than 64 bytes of data with one SPI command is unsupported")

        data_bits = len(data) * 8
        old_spi_usr = self.read_reg(SPI_USR_REG)
        old_spi_usr2 = self.read_reg(SPI_USR2_REG)
        flags = SPI_USR_COMMAND
        if read_bits > 0:
            flags |= SPI_USR_MISO
        if data_bits > 0:
            flags |= SPI_USR_MOSI
        set_data_lengths(data_bits, read_bits)
        self.write_reg(SPI_USR_REG, flags)
        self.write_reg(SPI_USR2_REG,
                       (7 << SPI_USR2_COMMAND_LEN_SHIFT) | spiflash_command)
        if data_bits == 0:
            self.write_reg(SPI_W0_REG, 0)  # clear data register before we read it
        else:
            data = pad_to(data, 4, b'\00')  # pad to 32-bit multiple
            words = struct.unpack("I" * (len(data) // 4), data)
            next_reg = SPI_W0_REG
            for word in words:
                self.write_reg(next_reg, word)
                next_reg += 4
        self.write_reg(SPI_CMD_REG, SPI_CMD_USR)

        def wait_done():
            for _ in range(10):
                if (self.read_reg(SPI_CMD_REG) & SPI_CMD_USR) == 0:
                    return
            raise FatalError("SPI command did not complete in time")
        wait_done()

        status = self.read_reg(SPI_W0_REG)
        # restore some SPI controller registers
        self.write_reg(SPI_USR_REG, old_spi_usr)
        self.write_reg(SPI_USR2_REG, old_spi_usr2)
        return status

    def read_status(self, num_bytes=2):
        """Read up to 24 bits (num_bytes) of SPI flash status register contents
        via RDSR, RDSR2, RDSR3 commands

        Not all SPI flash supports all three commands. The upper 1 or 2
        bytes may be 0xFF.
        """
        SPIFLASH_RDSR  = 0x05
        SPIFLASH_RDSR2 = 0x35
        SPIFLASH_RDSR3 = 0x15

        status = 0
        shift = 0
        for cmd in [SPIFLASH_RDSR, SPIFLASH_RDSR2, SPIFLASH_RDSR3][0:num_bytes]:
            status += self.run_spiflash_command(cmd, read_bits=8) << shift
            shift += 8
        return status

    def write_status(self, new_status, num_bytes=2, set_non_volatile=False):
        """Write up to 24 bits (num_bytes) of new status register

        num_bytes can be 1, 2 or 3.

        Not all flash supports the additional commands to write the
        second and third byte of the status register. When writing 2
        bytes, esptool also sends a 16-byte WRSR command (as some
        flash types use this instead of WRSR2.)

        If the set_non_volatile flag is set, non-volatile bits will
        be set as well as volatile ones (WREN used instead of WEVSR).

        """
        SPIFLASH_WRSR = 0x01
        SPIFLASH_WRSR2 = 0x31
        SPIFLASH_WRSR3 = 0x11
        SPIFLASH_WEVSR = 0x50
        SPIFLASH_WREN = 0x06
        SPIFLASH_WRDI = 0x04

        enable_cmd = SPIFLASH_WREN if set_non_volatile else SPIFLASH_WEVSR

        # try using a 16-bit WRSR (not supported by all chips)
        # this may be redundant, but shouldn't hurt
        if num_bytes == 2:
            self.run_spiflash_command(enable_cmd)
            self.run_spiflash_command(SPIFLASH_WRSR, struct.pack("<H", new_status))

        # also try using individual commands (also not supported by all chips for num_bytes 2 & 3)
        for cmd in [SPIFLASH_WRSR, SPIFLASH_WRSR2, SPIFLASH_WRSR3][0:num_bytes]:
            self.run_spiflash_command(enable_cmd)
            self.run_spiflash_command(cmd, struct.pack("B", new_status & 0xFF))
            new_status >>= 8

        self.run_spiflash_command(SPIFLASH_WRDI)

    def get_crystal_freq(self):
        # Figure out the crystal frequency from the UART clock divider
        # Returns a normalized value in integer MHz (40 or 26 are the only supported values)
        #
        # The logic here is:
        # - We know that our baud rate and the ESP UART baud rate are roughly the same, or we couldn't communicate
        # - We can read the UART clock divider register to know how the ESP derives this from the APB bus frequency
        # - Multiplying these two together gives us the bus frequency which is either the crystal frequency (ESP32)
        #   or double the crystal frequency (ESP8266). See the self.XTAL_CLK_DIVIDER parameter for this factor.
        uart_div = self.read_reg(self.UART_CLKDIV_REG) & self.UART_CLKDIV_MASK
        est_xtal = (self._port.baudrate * uart_div) / 1e6 / self.XTAL_CLK_DIVIDER
        norm_xtal = 40 if est_xtal > 33 else 26
        if abs(norm_xtal - est_xtal) > 1:
            kprint("WARNING: Detected crystal freq %.2fMHz is quite different to normalized freq %dMHz. Unsupported crystal in use?" % (est_xtal, norm_xtal))
        return norm_xtal

    def hard_reset(self):
        self._setRTS(True)  # EN->LOW
        time.sleep(0.1)
        self._setRTS(False)

    def soft_reset(self, stay_in_bootloader):
        if not self.IS_STUB:
            if stay_in_bootloader:
                return  # ROM bootloader is already in bootloader!
            else:
                # 'run user code' is as close to a soft reset as we can do
                self.flash_begin(0, 0)
                self.flash_finish(False)
        else:
            if stay_in_bootloader:
                # soft resetting from the stub loader
                # will re-load the ROM bootloader
                self.flash_begin(0, 0)
                self.flash_finish(True)
            elif self.CHIP_NAME != "ESP8266":
                raise FatalError("Soft resetting is currently only supported on ESP8266")
            else:
                # running user code from stub loader requires some hacks
                # in the stub loader
                self.command(self.ESP_RUN_USER_CODE, wait_response=False)


class ESP8266ROM(ESPLoader):
    """ Access class for ESP8266 ROM bootloader
    """
    CHIP_NAME = "ESP8266"
    IS_STUB = False

    DATE_REG_VALUE = 0x00062000
    DATE_REG2_VALUE = None

    # OTP ROM addresses
    ESP_OTP_MAC0    = 0x3ff00050
    ESP_OTP_MAC1    = 0x3ff00054
    ESP_OTP_MAC3    = 0x3ff0005c

    SPI_REG_BASE    = 0x60000200
    SPI_USR_OFFS    = 0x1c
    SPI_USR1_OFFS   = 0x20
    SPI_USR2_OFFS   = 0x24
    SPI_MOSI_DLEN_OFFS = None
    SPI_MISO_DLEN_OFFS = None
    SPI_W0_OFFS     = 0x40

    UART_CLKDIV_REG = 0x60000014

    XTAL_CLK_DIVIDER = 2

    FLASH_SIZES = {
        '512KB':0x00,
        '256KB':0x10,
        '1MB':0x20,
        '2MB':0x30,
        '4MB':0x40,
        '2MB-c1': 0x50,
        '4MB-c1':0x60,
        '8MB':0x80,
        '16MB':0x90,
    }

    BOOTLOADER_FLASH_OFFSET = 0

    MEMORY_MAP = [[0x3FF00000, 0x3FF00010, "DPORT"],
                  [0x3FFE8000, 0x40000000, "DRAM"],
                  [0x40100000, 0x40108000, "IRAM"],
                  [0x40201010, 0x402E1010, "IROM"]]

    def get_efuses(self):
        # Return the 128 bits of ESP8266 efuse as a single Python integer
        return (self.read_reg(0x3ff0005c) << 96 |
                self.read_reg(0x3ff00058) << 64 |
                self.read_reg(0x3ff00054) << 32 |
                self.read_reg(0x3ff00050))

    def get_chip_description(self):
        efuses = self.get_efuses()
        is_8285 = (efuses & ((1 << 4) | 1 << 80)) != 0  # One or the other efuse bit is set for ESP8285
        return "ESP8285" if is_8285 else "ESP8266EX"

    def get_chip_features(self):
        features = ["WiFi"]
        if self.get_chip_description() == "ESP8285":
            features += ["Embedded Flash"]
        return features

    def flash_spi_attach(self, hspi_arg):
        if self.IS_STUB:
            super(ESP8266ROM, self).flash_spi_attach(hspi_arg)
        else:
            # ESP8266 ROM has no flash_spi_attach command in serial protocol,
            # but flash_begin will do it
            self.flash_begin(0, 0)

    def flash_set_parameters(self, size):
        # not implemented in ROM, but OK to silently skip for ROM
        if self.IS_STUB:
            super(ESP8266ROM, self).flash_set_parameters(size)

    def chip_id(self):
        """ Read Chip ID from efuse - the equivalent of the SDK system_get_chip_id() function """
        id0 = self.read_reg(self.ESP_OTP_MAC0)
        id1 = self.read_reg(self.ESP_OTP_MAC1)
        return (id0 >> 24) | ((id1 & MAX_UINT24) << 8)

    def read_mac(self):
        """ Read MAC from OTP ROM """
        mac0 = self.read_reg(self.ESP_OTP_MAC0)
        mac1 = self.read_reg(self.ESP_OTP_MAC1)
        mac3 = self.read_reg(self.ESP_OTP_MAC3)
        if (mac3 != 0):
            oui = ((mac3 >> 16) & 0xff, (mac3 >> 8) & 0xff, mac3 & 0xff)
        elif ((mac1 >> 16) & 0xff) == 0:
            oui = (0x18, 0xfe, 0x34)
        elif ((mac1 >> 16) & 0xff) == 1:
            oui = (0xac, 0xd0, 0x74)
        else:
            raise FatalError("Unknown OUI")
        return oui + ((mac1 >> 8) & 0xff, mac1 & 0xff, (mac0 >> 24) & 0xff)

    def get_erase_size(self, offset, size):
        """ Calculate an erase size given a specific size in bytes.

        Provides a workaround for the bootloader erase bug."""

        sectors_per_block = 16
        sector_size = self.FLASH_SECTOR_SIZE
        num_sectors = (size + sector_size - 1) // sector_size
        start_sector = offset // sector_size

        head_sectors = sectors_per_block - (start_sector % sectors_per_block)
        if num_sectors < head_sectors:
            head_sectors = num_sectors

        if num_sectors < 2 * head_sectors:
            return (num_sectors + 1) // 2 * sector_size
        else:
            return (num_sectors - head_sectors) * sector_size

    def override_vddsdio(self, new_voltage):
        raise NotImplementedInROMError("Overriding VDDSDIO setting only applies to ESP32")


class ESP8266StubLoader(ESP8266ROM):
    """ Access class for ESP8266 stub loader, runs on top of ROM.
    """
    FLASH_WRITE_SIZE = 0x4000  # matches MAX_WRITE_BLOCK in stub_loader.c
    IS_STUB = True

    def __init__(self, rom_loader):
        self._port = rom_loader._port
        self._trace_enabled = rom_loader._trace_enabled
        self.flush_input()  # resets _slip_reader

    def get_erase_size(self, offset, size):
        return size  # stub doesn't have same size bug as ROM loader


ESP8266ROM.STUB_CLASS = ESP8266StubLoader


class ESP32ROM(ESPLoader):
    """Access class for ESP32 ROM bootloader

    """
    CHIP_NAME = "ESP32"
    IMAGE_CHIP_ID = 0
    IS_STUB = False

    DATE_REG_VALUE = 0x15122500
    DATE_REG2_VALUE = None

    IROM_MAP_START = 0x400d0000
    IROM_MAP_END   = 0x40400000

    DROM_MAP_START = 0x3F400000
    DROM_MAP_END   = 0x3F800000

    # ESP32 uses a 4 byte status reply
    STATUS_BYTES_LENGTH = 4

    SPI_REG_BASE   = 0x60002000
    SPI_USR_OFFS    = 0x1c
    SPI_USR1_OFFS   = 0x20
    SPI_USR2_OFFS   = 0x24
    SPI_MOSI_DLEN_OFFS = 0x28
    SPI_MISO_DLEN_OFFS = 0x2c
    EFUSE_RD_REG_BASE = 0x6001a000

    EFUSE_DIS_DOWNLOAD_MANUAL_ENCRYPT_REG = EFUSE_RD_REG_BASE + 0x18
    EFUSE_DIS_DOWNLOAD_MANUAL_ENCRYPT = (1 << 7)  # EFUSE_RD_DISABLE_DL_ENCRYPT

    DR_REG_SYSCON_BASE = 0x3ff66000

    SPI_W0_OFFS = 0x80

    UART_CLKDIV_REG = 0x3ff40014

    XTAL_CLK_DIVIDER = 1

    FLASH_SIZES = {
        '1MB':0x00,
        '2MB':0x10,
        '4MB':0x20,
        '8MB':0x30,
        '16MB':0x40
    }

    BOOTLOADER_FLASH_OFFSET = 0x1000

    OVERRIDE_VDDSDIO_CHOICES = ["1.8V", "1.9V", "OFF"]

    MEMORY_MAP = [[0x3F400000, 0x3F800000, "DROM"],
                  [0x3F800000, 0x3FC00000, "EXTRAM_DATA"],
                  [0x3FF80000, 0x3FF82000, "RTC_DRAM"],
                  [0x3FF90000, 0x40000000, "BYTE_ACCESSIBLE"],
                  [0x3FFAE000, 0x40000000, "DRAM"],
                  [0x3FFAE000, 0x40000000, "DMA"],
                  [0x3FFE0000, 0x3FFFFFFC, "DIRAM_DRAM"],
                  [0x40000000, 0x40070000, "IROM"],
                  [0x40070000, 0x40078000, "CACHE_PRO"],
                  [0x40078000, 0x40080000, "CACHE_APP"],
                  [0x40080000, 0x400A0000, "IRAM"],
                  [0x400A0000, 0x400BFFFC, "DIRAM_IRAM"],
                  [0x400C0000, 0x400C2000, "RTC_IRAM"],
                  [0x400D0000, 0x40400000, "IROM"],
                  [0x50000000, 0x50002000, "RTC_DATA"]]

    FLASH_ENCRYPTED_WRITE_ALIGN = 32

    _trace_enabled = False

    """ Try to read the BLOCK1 (encryption key) and check if it is valid """

    def is_flash_encryption_key_valid(self):

        """ Bit 0 of efuse_rd_disable[3:0] is mapped to BLOCK1
        this bit is at position 16 in EFUSE_BLK0_RDATA0_REG """
        word0 = self.read_efuse(0)
        rd_disable = (word0 >> 16) & 0x1

        # reading of BLOCK1 is NOT ALLOWED so we assume valid key is programmed
        if rd_disable:
            return True
        else:
            # reading of BLOCK1 is ALLOWED so we will read and verify for non-zero.
            # When ESP32 has not generated AES/encryption key in BLOCK1, the contents will be readable and 0.
            # If the flash encryption is enabled it is expected to have a valid non-zero key. We break out on
            # first occurance of non-zero value
            key_word = [0] * 7
            for i in range(len(key_word)):
                key_word[i] = self.read_efuse(14 + i)
                # key is non-zero so break & return
                if key_word[i] != 0:
                    return True
            return False

    def get_flash_crypt_config(self):
        """ For flash encryption related commands we need to make sure
        user has programmed all the relevant efuse correctly so before
        writing encrypted write_flash_encrypt esptool will verify the values
        of flash_crypt_config to be non zero if they are not read
        protected. If the values are zero a warning will be kprinted

        bit 3 in efuse_rd_disable[3:0] is mapped to flash_crypt_config
        this bit is at position 19 in EFUSE_BLK0_RDATA0_REG """
        word0 = self.read_efuse(0)
        rd_disable = (word0 >> 19) & 0x1

        if rd_disable == 0:
            """ we can read the flash_crypt_config efuse value
            so go & read it (EFUSE_BLK0_RDATA5_REG[31:28]) """
            word5 = self.read_efuse(5)
            word5 = (word5 >> 28) & 0xF
            return word5
        else:
            # if read of the efuse is disabled we assume it is set correctly
            return 0xF

    def get_encrypted_download_disabled(self):
        if self.read_reg(self.EFUSE_DIS_DOWNLOAD_MANUAL_ENCRYPT_REG) & self.EFUSE_DIS_DOWNLOAD_MANUAL_ENCRYPT:
            return True
        else:
            return False

    def get_chip_description(self):
        word3 = self.read_efuse(3)
        word5 = self.read_efuse(5)
        apb_ctl_date = self.read_reg(self.DR_REG_SYSCON_BASE + 0x7C)
        rev_bit0 = (word3 >> 15) & 0x1
        rev_bit1 = (word5 >> 20) & 0x1
        rev_bit2 = (apb_ctl_date >> 31) & 0x1
        pkg_version = (word3 >> 9) & 0x07

        chip_name = {
            0: "ESP32D0WDQ6",
            1: "ESP32D0WDQ5",
            2: "ESP32D2WDQ5",
            5: "ESP32-PICO-D4",
        }.get(pkg_version, "unknown ESP32")

        chip_revision = 0
        if rev_bit0:
            if rev_bit1:
                if rev_bit2:
                    chip_revision = 3
                else:
                    chip_revision = 2
            else:
                chip_revision = 1
        return "%s (revision %d)" % (chip_name, chip_revision)

    def get_chip_features(self):
        features = ["WiFi"]
        word3 = self.read_efuse(3)

        # names of variables in this section are lowercase
        #  versions of EFUSE names as documented in TRM and
        # ESP-IDF efuse_reg.h

        chip_ver_dis_bt = word3 & (1 << 1)
        if chip_ver_dis_bt == 0:
            features += ["BT"]

        chip_ver_dis_app_cpu = word3 & (1 << 0)
        if chip_ver_dis_app_cpu:
            features += ["Single Core"]
        else:
            features += ["Dual Core"]

        chip_cpu_freq_rated = word3 & (1 << 13)
        if chip_cpu_freq_rated:
            chip_cpu_freq_low = word3 & (1 << 12)
            if chip_cpu_freq_low:
                features += ["160MHz"]
            else:
                features += ["240MHz"]

        pkg_version = (word3 >> 9) & 0x07
        if pkg_version in [2, 4, 5]:
            features += ["Embedded Flash"]

        word4 = self.read_efuse(4)
        adc_vref = (word4 >> 8) & 0x1F
        if adc_vref:
            features += ["VRef calibration in efuse"]

        blk3_part_res = word3 >> 14 & 0x1
        if blk3_part_res:
            features += ["BLK3 partially reserved"]

        word6 = self.read_efuse(6)
        coding_scheme = word6 & 0x3
        features += ["Coding Scheme %s" % {
            0: "None",
            1: "3/4",
            2: "Repeat (UNSUPPORTED)",
            3: "Invalid"}[coding_scheme]]

        return features

    def read_efuse(self, n):
        """ Read the nth word of the ESP3x EFUSE region. """
        return self.read_reg(self.EFUSE_RD_REG_BASE + (4 * n))

    def chip_id(self):
        raise NotSupportedError(self, "chip_id")

    def read_mac(self):
        """ Read MAC from EFUSE region """
        words = [self.read_efuse(2), self.read_efuse(1)]
        bitstring = struct.pack(">II", *words)
        bitstring = bitstring[2:8]  # trim the 2 byte CRC
        try:
            return tuple(ord(b) for b in bitstring)
        except TypeError:  # Python 3, bitstring elements are already bytes
            return tuple(bitstring)

    def get_erase_size(self, offset, size):
        return size

    def override_vddsdio(self, new_voltage):
        new_voltage = new_voltage.upper()
        if new_voltage not in self.OVERRIDE_VDDSDIO_CHOICES:
            raise FatalError("The only accepted VDDSDIO overrides are '1.8V', '1.9V' and 'OFF'")
        RTC_CNTL_SDIO_CONF_REG = 0x3ff48074
        RTC_CNTL_XPD_SDIO_REG = (1 << 31)
        RTC_CNTL_DREFH_SDIO_M = (3 << 29)
        RTC_CNTL_DREFM_SDIO_M = (3 << 27)
        RTC_CNTL_DREFL_SDIO_M = (3 << 25)
        # RTC_CNTL_SDIO_TIEH = (1 << 23)  # not used here, setting TIEH=1 would set 3.3V output, not safe for esptool.py to do
        RTC_CNTL_SDIO_FORCE = (1 << 22)
        RTC_CNTL_SDIO_PD_EN = (1 << 21)

        reg_val = RTC_CNTL_SDIO_FORCE  # override efuse setting
        reg_val |= RTC_CNTL_SDIO_PD_EN
        if new_voltage != "OFF":
            reg_val |= RTC_CNTL_XPD_SDIO_REG  # enable internal LDO
        if new_voltage == "1.9V":
            reg_val |= (RTC_CNTL_DREFH_SDIO_M | RTC_CNTL_DREFM_SDIO_M | RTC_CNTL_DREFL_SDIO_M)  # boost voltage
        self.write_reg(RTC_CNTL_SDIO_CONF_REG, reg_val)
        kprint("VDDSDIO regulator set to %s" % new_voltage)

    def read_flash_slow(self, offset, length, progress_fn):
        BLOCK_LEN = 64  # ROM read limit per command (this limit is why it's so slow)

        data = b''
        while len(data) < length:
            block_len = min(BLOCK_LEN, length - len(data))
            r = self.check_command("read flash block", self.ESP_READ_FLASH_SLOW,
                                   struct.pack('<II', offset + len(data), block_len))
            if len(r) < block_len:
                raise FatalError("Expected %d byte block, got %d bytes. Serial errors?" % (block_len, len(r)))
            data += r[:block_len]  # command always returns 64 byte buffer, regardless of how many bytes were actually read from flash
            if progress_fn and (len(data) % 1024 == 0 or len(data) == length):
                progress_fn(len(data), length)
        return data


class ESP32S2ROM(ESP32ROM):
    CHIP_NAME = "ESP32-S2"
    IMAGE_CHIP_ID = 2

    IROM_MAP_START = 0x40080000
    IROM_MAP_END   = 0x40b80000
    DROM_MAP_START = 0x3F000000
    DROM_MAP_END   = 0x3F3F0000

    DATE_REG_VALUE = 0x00000500   # This is actually UART_ID_REG(0) on ESP32-S2
    DATE_REG2_VALUE = 0x19031400  # this is the date register

    SPI_REG_BASE = 0x3f402000
    SPI_USR_OFFS    = 0x18
    SPI_USR1_OFFS   = 0x1c
    SPI_USR2_OFFS   = 0x20
    SPI_MOSI_DLEN_OFFS = 0x24
    SPI_MISO_DLEN_OFFS = 0x28
    SPI_W0_OFFS = 0x58

    MAC_EFUSE_REG = 0x3f41A044  # ESP32-S2 has special block for MAC efuses

    UART_CLKDIV_REG = 0x3f400014

    FLASH_ENCRYPTED_WRITE_ALIGN = 16

    # todo: use espefuse APIs to get this info
    EFUSE_BASE = 0x3f41A000
    EFUSE_RD_REG_BASE = EFUSE_BASE + 0x030  # BLOCK0 read base address

    EFUSE_PURPOSE_KEY0_REG = EFUSE_BASE + 0x34
    EFUSE_PURPOSE_KEY0_SHIFT = 24
    EFUSE_PURPOSE_KEY1_REG = EFUSE_BASE + 0x34
    EFUSE_PURPOSE_KEY1_SHIFT = 28
    EFUSE_PURPOSE_KEY2_REG = EFUSE_BASE + 0x38
    EFUSE_PURPOSE_KEY2_SHIFT = 0
    EFUSE_PURPOSE_KEY3_REG = EFUSE_BASE + 0x38
    EFUSE_PURPOSE_KEY3_SHIFT = 4
    EFUSE_PURPOSE_KEY4_REG = EFUSE_BASE + 0x38
    EFUSE_PURPOSE_KEY4_SHIFT = 8
    EFUSE_PURPOSE_KEY5_REG = EFUSE_BASE + 0x38
    EFUSE_PURPOSE_KEY5_SHIFT = 12

    EFUSE_DIS_DOWNLOAD_MANUAL_ENCRYPT_REG = EFUSE_RD_REG_BASE
    EFUSE_DIS_DOWNLOAD_MANUAL_ENCRYPT = 1 << 19

    PURPOSE_VAL_XTS_AES256_KEY_1 = 2
    PURPOSE_VAL_XTS_AES256_KEY_2 = 3
    PURPOSE_VAL_XTS_AES128_KEY = 4

    def get_chip_description(self):
        return "ESP32-S2"

    def get_chip_features(self):
        return ["WiFi"]

    def get_crystal_freq(self):
        # ESP32-S2 XTAL is fixed to 40MHz
        return 40

    def override_vddsdio(self, new_voltage):
        raise NotImplementedInROMError("VDD_SDIO overrides are not supported for ESP32-S2")

    def read_mac(self):
        mac0 = self.read_reg(self.MAC_EFUSE_REG)
        mac1 = self.read_reg(self.MAC_EFUSE_REG + 4)  # only bottom 16 bits are MAC
        bitstring = struct.pack(">II", mac1, mac0)[2:]
        try:
            return tuple(ord(b) for b in bitstring)
        except TypeError:  # Python 3, bitstring elements are already bytes
            return tuple(bitstring)

    def get_flash_crypt_config(self):
        return None  # doesn't exist on ESP32-S2

    def get_key_block_purpose(self, key_block):
        if key_block < 0 or key_block > 5:
            raise FatalError("Valid key block numbers must be in range 0-5")

        reg, shift = [(self.EFUSE_PURPOSE_KEY0_REG, self.EFUSE_PURPOSE_KEY0_SHIFT),
                      (self.EFUSE_PURPOSE_KEY1_REG, self.EFUSE_PURPOSE_KEY1_SHIFT),
                      (self.EFUSE_PURPOSE_KEY2_REG, self.EFUSE_PURPOSE_KEY2_SHIFT),
                      (self.EFUSE_PURPOSE_KEY3_REG, self.EFUSE_PURPOSE_KEY3_SHIFT),
                      (self.EFUSE_PURPOSE_KEY4_REG, self.EFUSE_PURPOSE_KEY4_SHIFT),
                      (self.EFUSE_PURPOSE_KEY5_REG, self.EFUSE_PURPOSE_KEY5_SHIFT)][key_block]
        return (self.read_reg(reg) >> shift) & 0xF

    def is_flash_encryption_key_valid(self):
        # Need to see either an AES-128 key or two AES-256 keys
        purposes = [self.get_key_block_purpose(b) for b in range(6)]

        if any(p == self.PURPOSE_VAL_XTS_AES128_KEY for p in purposes):
            return True

        return any(p == self.PURPOSE_VAL_XTS_AES256_KEY_1 for p in purposes) \
            and any(p == self.PURPOSE_VAL_XTS_AES256_KEY_2 for p in purposes)


class ESP32StubLoader(ESP32ROM):
    """ Access class for ESP32 stub loader, runs on top of ROM.
    """
    FLASH_WRITE_SIZE = 0x4000  # matches MAX_WRITE_BLOCK in stub_loader.c
    STATUS_BYTES_LENGTH = 2  # same as ESP8266, different to ESP32 ROM
    IS_STUB = True

    def __init__(self, rom_loader):
        self._port = rom_loader._port
        self._trace_enabled = rom_loader._trace_enabled
        self.flush_input()  # resets _slip_reader


ESP32ROM.STUB_CLASS = ESP32StubLoader


class ESP32S2StubLoader(ESP32S2ROM):
    """ Access class for ESP32-S2 stub loader, runs on top of ROM.

    (Basically the same as ESP2StubLoader, but different base class.
    Can possibly be made into a mixin.)
    """
    FLASH_WRITE_SIZE = 0x4000  # matches MAX_WRITE_BLOCK in stub_loader.c
    STATUS_BYTES_LENGTH = 2  # same as ESP8266, different to ESP32 ROM
    IS_STUB = True

    def __init__(self, rom_loader):
        self._port = rom_loader._port
        self._trace_enabled = rom_loader._trace_enabled
        self.flush_input()  # resets _slip_reader


ESP32S2ROM.STUB_CLASS = ESP32S2StubLoader


class ESPBOOTLOADER(object):
    """ These are constants related to software ESP bootloader, working with 'v2' image files """

    # First byte of the "v2" application image
    IMAGE_V2_MAGIC = 0xea

    # First 'segment' value in a "v2" application image, appears to be a constant version value?
    IMAGE_V2_SEGMENT = 4


def LoadFirmwareImage(chip, filename):
    """ Load a firmware image. Can be for any supported SoC.

        ESP8266 images will be examined to determine if they are original ROM firmware images (ESP8266ROMFirmwareImage)
        or "v2" OTA bootloader images.

        Returns a BaseFirmwareImage subclass, either ESP8266ROMFirmwareImage (v1) or ESP8266V2FirmwareImage (v2).
    """
    chip = chip.lower().replace("-", "")
    with open(filename, 'rb') as f:
        if chip == 'esp32':
            return ESP32FirmwareImage(f)
        elif chip == "esp32s2":
            return ESP32S2FirmwareImage(f)
        else:  # Otherwise, ESP8266 so look at magic to determine the image type
            magic = ord(f.read(1))
            f.seek(0)
            if magic == ESPLoader.ESP_IMAGE_MAGIC:
                return ESP8266ROMFirmwareImage(f)
            elif magic == ESPBOOTLOADER.IMAGE_V2_MAGIC:
                return ESP8266V2FirmwareImage(f)
            else:
                raise FatalError("Invalid image magic number: %d" % magic)


class ImageSegment(object):
    """ Wrapper class for a segment in an ESP image
    (very similar to a section in an ELFImage also) """
    def __init__(self, addr, data, file_offs=None):
        self.addr = addr
        self.data = data
        self.file_offs = file_offs
        self.include_in_checksum = True
        if self.addr != 0:
            self.pad_to_alignment(4)  # pad all "real" ImageSegments 4 byte aligned length

    def copy_with_new_addr(self, new_addr):
        """ Return a new ImageSegment with same data, but mapped at
        a new address. """
        return ImageSegment(new_addr, self.data, 0)

    def split_image(self, split_len):
        """ Return a new ImageSegment which splits "split_len" bytes
        from the beginning of the data. Remaining bytes are kept in
        this segment object (and the start address is adjusted to match.) """
        result = copy.copy(self)
        result.data = self.data[:split_len]
        self.data = self.data[split_len:]
        self.addr += split_len
        self.file_offs = None
        result.file_offs = None
        return result

    def __repr__(self):
        r = "len 0x%05x load 0x%08x" % (len(self.data), self.addr)
        if self.file_offs is not None:
            r += " file_offs 0x%08x" % (self.file_offs)
        return r

    def pad_to_alignment(self, alignment):
        self.data = pad_to(self.data, alignment, b'\x00')


class ELFSection(ImageSegment):
    """ Wrapper class for a section in an ELF image, has a section
    name as well as the common properties of an ImageSegment. """
    def __init__(self, name, addr, data):
        super(ELFSection, self).__init__(addr, data)
        self.name = name.decode("utf-8")

    def __repr__(self):
        return "%s %s" % (self.name, super(ELFSection, self).__repr__())


class BaseFirmwareImage(object):
    SEG_HEADER_LEN = 8
    SHA256_DIGEST_LEN = 32

    """ Base class with common firmware image functions """
    def __init__(self):
        self.segments = []
        self.entrypoint = 0
        self.elf_sha256 = None
        self.elf_sha256_offset = 0

    def load_common_header(self, load_file, expected_magic):
        (magic, segments, self.flash_mode, self.flash_size_freq, self.entrypoint) = struct.unpack('<BBBBI', load_file.read(8))

        if magic != expected_magic:
            raise FatalError('Invalid firmware image magic=0x%x' % (magic))
        return segments

    def verify(self):
        if len(self.segments) > 16:
            raise FatalError('Invalid segment count %d (max 16). Usually this indicates a linker script problem.' % len(self.segments))

    def load_segment(self, f, is_irom_segment=False):
        """ Load the next segment from the image file """
        file_offs = f.tell()
        (offset, size) = struct.unpack('<II', f.read(8))
        self.warn_if_unusual_segment(offset, size, is_irom_segment)
        segment_data = f.read(size)
        if len(segment_data) < size:
            raise FatalError('End of file reading segment 0x%x, length %d (actual length %d)' % (offset, size, len(segment_data)))
        segment = ImageSegment(offset, segment_data, file_offs)
        self.segments.append(segment)
        return segment

    def warn_if_unusual_segment(self, offset, size, is_irom_segment):
        if not is_irom_segment:
            if offset > 0x40200000 or offset < 0x3ffe0000 or size > 65536:
                kprint('WARNING: Suspicious segment 0x%x, length %d' % (offset, size))

    def maybe_patch_segment_data(self, f, segment_data):
        """If SHA256 digest of the ELF file needs to be inserted into this segment, do so. Returns segment data."""
        segment_len = len(segment_data)
        file_pos = f.tell()  # file_pos is position in the .bin file
        if self.elf_sha256_offset >= file_pos and self.elf_sha256_offset < file_pos + segment_len:
            # SHA256 digest needs to be patched into this binary segment,
            # calculate offset of the digest inside the binary segment.
            patch_offset = self.elf_sha256_offset - file_pos
            # Sanity checks
            if patch_offset < self.SEG_HEADER_LEN or patch_offset + self.SHA256_DIGEST_LEN > segment_len:
                raise FatalError('Cannot place SHA256 digest on segment boundary' +
                                 '(elf_sha256_offset=%d, file_pos=%d, segment_size=%d)' %
                                 (self.elf_sha256_offset, file_pos, segment_len))
            if segment_data[patch_offset:patch_offset + self.SHA256_DIGEST_LEN] != b'\x00' * self.SHA256_DIGEST_LEN:
                raise FatalError('Contents of segment at SHA256 digest offset 0x%x are not all zero. Refusing to overwrite.' %
                                 self.elf_sha256_offset)
            assert(len(self.elf_sha256) == self.SHA256_DIGEST_LEN)
            # offset relative to the data part
            patch_offset -= self.SEG_HEADER_LEN
            segment_data = segment_data[0:patch_offset] + self.elf_sha256 + \
                segment_data[patch_offset + self.SHA256_DIGEST_LEN:]
        return segment_data

    def save_segment(self, f, segment, checksum=None):
        """ Save the next segment to the image file, return next checksum value if provided """
        segment_data = self.maybe_patch_segment_data(f, segment.data)
        f.write(struct.pack('<II', segment.addr, len(segment_data)))
        f.write(segment_data)
        if checksum is not None:
            return ESPLoader.checksum(segment_data, checksum)

    def read_checksum(self, f):
        """ Return ESPLoader checksum from end of just-read image """
        # Skip the padding. The checksum is stored in the last byte so that the
        # file is a multiple of 16 bytes.
        align_file_position(f, 16)
        return ord(f.read(1))

    def calculate_checksum(self):
        """ Calculate checksum of loaded image, based on segments in
        segment array.
        """
        checksum = ESPLoader.ESP_CHECKSUM_MAGIC
        for seg in self.segments:
            if seg.include_in_checksum:
                checksum = ESPLoader.checksum(seg.data, checksum)
        return checksum

    def append_checksum(self, f, checksum):
        """ Append ESPLoader checksum to the just-written image """
        align_file_position(f, 16)
        f.write(struct.pack(b'B', checksum))

    def write_common_header(self, f, segments):
        f.write(struct.pack('<BBBBI', ESPLoader.ESP_IMAGE_MAGIC, len(segments),
                            self.flash_mode, self.flash_size_freq, self.entrypoint))

    def is_irom_addr(self, addr):
        """ Returns True if an address starts in the irom region.
        Valid for ESP8266 only.
        """
        return ESP8266ROM.IROM_MAP_START <= addr < ESP8266ROM.IROM_MAP_END

    def get_irom_segment(self):
        irom_segments = [s for s in self.segments if self.is_irom_addr(s.addr)]
        if len(irom_segments) > 0:
            if len(irom_segments) != 1:
                raise FatalError('Found %d segments that could be irom0. Bad ELF file?' % len(irom_segments))
            return irom_segments[0]
        return None

    def get_non_irom_segments(self):
        irom_segment = self.get_irom_segment()
        return [s for s in self.segments if s != irom_segment]


class ESP8266ROMFirmwareImage(BaseFirmwareImage):
    """ 'Version 1' firmware image, segments loaded directly by the ROM bootloader. """

    ROM_LOADER = ESP8266ROM

    def __init__(self, load_file=None):
        super(ESP8266ROMFirmwareImage, self).__init__()
        self.flash_mode = 0
        self.flash_size_freq = 0
        self.version = 1

        if load_file is not None:
            segments = self.load_common_header(load_file, ESPLoader.ESP_IMAGE_MAGIC)

            for _ in range(segments):
                self.load_segment(load_file)
            self.checksum = self.read_checksum(load_file)

            self.verify()

    def default_output_name(self, input_file):
        """ Derive a default output name from the ELF name. """
        return input_file + '-'

    def save(self, basename):
        """ Save a set of V1 images for flashing. Parameter is a base filename. """
        # IROM data goes in its own plain binary file
        irom_segment = self.get_irom_segment()
        if irom_segment is not None:
            with open("%s0x%05x.bin" % (basename, irom_segment.addr - ESP8266ROM.IROM_MAP_START), "wb") as f:
                f.write(irom_segment.data)

        # everything but IROM goes at 0x00000 in an image file
        normal_segments = self.get_non_irom_segments()
        with open("%s0x00000.bin" % basename, 'wb') as f:
            self.write_common_header(f, normal_segments)
            checksum = ESPLoader.ESP_CHECKSUM_MAGIC
            for segment in normal_segments:
                checksum = self.save_segment(f, segment, checksum)
            self.append_checksum(f, checksum)


ESP8266ROM.BOOTLOADER_IMAGE = ESP8266ROMFirmwareImage


class ESP8266V2FirmwareImage(BaseFirmwareImage):
    """ 'Version 2' firmware image, segments loaded by software bootloader stub
        (ie Espressif bootloader or rboot)
    """

    ROM_LOADER = ESP8266ROM

    def __init__(self, load_file=None):
        super(ESP8266V2FirmwareImage, self).__init__()
        self.version = 2
        if load_file is not None:
            segments = self.load_common_header(load_file, ESPBOOTLOADER.IMAGE_V2_MAGIC)
            if segments != ESPBOOTLOADER.IMAGE_V2_SEGMENT:
                # segment count is not really segment count here, but we expect to see '4'
                kprint('Warning: V2 header has unexpected "segment" count %d (usually 4)' % segments)

            # irom segment comes before the second header
            #
            # the file is saved in the image with a zero load address
            # in the header, so we need to calculate a load address
            irom_segment = self.load_segment(load_file, True)
            irom_segment.addr = 0  # for actual mapped addr, add ESP8266ROM.IROM_MAP_START + flashing_addr + 8
            irom_segment.include_in_checksum = False

            first_flash_mode = self.flash_mode
            first_flash_size_freq = self.flash_size_freq
            first_entrypoint = self.entrypoint
            # load the second header

            segments = self.load_common_header(load_file, ESPLoader.ESP_IMAGE_MAGIC)

            if first_flash_mode != self.flash_mode:
                kprint('WARNING: Flash mode value in first header (0x%02x) disagrees with second (0x%02x). Using second value.'
                      % (first_flash_mode, self.flash_mode))
            if first_flash_size_freq != self.flash_size_freq:
                kprint('WARNING: Flash size/freq value in first header (0x%02x) disagrees with second (0x%02x). Using second value.'
                      % (first_flash_size_freq, self.flash_size_freq))
            if first_entrypoint != self.entrypoint:
                kprint('WARNING: Entrypoint address in first header (0x%08x) disagrees with second header (0x%08x). Using second value.'
                      % (first_entrypoint, self.entrypoint))

            # load all the usual segments
            for _ in range(segments):
                self.load_segment(load_file)
            self.checksum = self.read_checksum(load_file)

            self.verify()

    def default_output_name(self, input_file):
        """ Derive a default output name from the ELF name. """
        irom_segment = self.get_irom_segment()
        if irom_segment is not None:
            irom_offs = irom_segment.addr - ESP8266ROM.IROM_MAP_START
        else:
            irom_offs = 0
        return "%s-0x%05x.bin" % (os.path.splitext(input_file)[0],
                                  irom_offs & ~(ESPLoader.FLASH_SECTOR_SIZE - 1))

    def save(self, filename):
        with open(filename, 'wb') as f:
            # Save first header for irom0 segment
            f.write(struct.pack(b'<BBBBI', ESPBOOTLOADER.IMAGE_V2_MAGIC, ESPBOOTLOADER.IMAGE_V2_SEGMENT,
                                self.flash_mode, self.flash_size_freq, self.entrypoint))

            irom_segment = self.get_irom_segment()
            if irom_segment is not None:
                # save irom0 segment, make sure it has load addr 0 in the file
                irom_segment = irom_segment.copy_with_new_addr(0)
                irom_segment.pad_to_alignment(16)  # irom_segment must end on a 16 byte boundary
                self.save_segment(f, irom_segment)

            # second header, matches V1 header and contains loadable segments
            normal_segments = self.get_non_irom_segments()
            self.write_common_header(f, normal_segments)
            checksum = ESPLoader.ESP_CHECKSUM_MAGIC
            for segment in normal_segments:
                checksum = self.save_segment(f, segment, checksum)
            self.append_checksum(f, checksum)

        # calculate a crc32 of entire file and append
        # (algorithm used by recent 8266 SDK bootloaders)
        with open(filename, 'rb') as f:
            crc = esp8266_crc32(f.read())
        with open(filename, 'ab') as f:
            f.write(struct.pack(b'<I', crc))


# Backwards compatibility for previous API, remove in esptool.py V3
ESPFirmwareImage = ESP8266ROMFirmwareImage
OTAFirmwareImage = ESP8266V2FirmwareImage


def esp8266_crc32(data):
    """
    CRC32 algorithm used by 8266 SDK bootloader (and gen_appbin.py).
    """
    crc = binascii.crc32(data, 0) & 0xFFFFFFFF
    if crc & 0x80000000:
        return crc ^ 0xFFFFFFFF
    else:
        return crc + 1


class ESP32FirmwareImage(BaseFirmwareImage):
    """ ESP32 firmware image is very similar to V1 ESP8266 image,
    except with an additional 16 byte reserved header at top of image,
    and because of new flash mapping capabilities the flash-mapped regions
    can be placed in the normal image (just @ 64kB padded offsets).
    """

    ROM_LOADER = ESP32ROM

    # ROM bootloader will read the wp_pin field if SPI flash
    # pins are remapped via flash. IDF actually enables QIO only
    # from software bootloader, so this can be ignored. But needs
    # to be set to this value so ROM bootloader will skip it.
    WP_PIN_DISABLED = 0xEE

    EXTENDED_HEADER_STRUCT_FMT = "<BBBBHB" + ("B" * 8) + "B"

    IROM_ALIGN = 65536

    def __init__(self, load_file=None):
        super(ESP32FirmwareImage, self).__init__()
        self.secure_pad = None
        self.flash_mode = 0
        self.flash_size_freq = 0
        self.version = 1
        self.wp_pin = self.WP_PIN_DISABLED
        # SPI pin drive levels
        self.clk_drv = 0
        self.q_drv = 0
        self.d_drv = 0
        self.cs_drv = 0
        self.hd_drv = 0
        self.wp_drv = 0
        self.min_rev = 0

        self.append_digest = True

        if load_file is not None:
            start = load_file.tell()

            segments = self.load_common_header(load_file, ESPLoader.ESP_IMAGE_MAGIC)
            self.load_extended_header(load_file)

            for _ in range(segments):
                self.load_segment(load_file)
            self.checksum = self.read_checksum(load_file)

            if self.append_digest:
                end = load_file.tell()
                self.stored_digest = load_file.read(32)
                load_file.seek(start)
                calc_digest = hashlib.sha256()
                calc_digest.update(load_file.read(end - start))
                self.calc_digest = calc_digest.digest()  # TODO: decide what to do here?

            self.verify()

    def is_flash_addr(self, addr):
        return (self.ROM_LOADER.IROM_MAP_START <= addr < self.ROM_LOADER.IROM_MAP_END) \
            or (self.ROM_LOADER.DROM_MAP_START <= addr < self.ROM_LOADER.DROM_MAP_END)

    def default_output_name(self, input_file):
        """ Derive a default output name from the ELF name. """
        return "%s.bin" % (os.path.splitext(input_file)[0])

    def warn_if_unusual_segment(self, offset, size, is_irom_segment):
        pass  # TODO: add warnings for ESP32 segment offset/size combinations that are wrong

    def save(self, filename):
        total_segments = 0
        with io.BytesIO() as f:  # write file to memory first
            self.write_common_header(f, self.segments)

            # first 4 bytes of header are read by ROM bootloader for SPI
            # config, but currently unused
            self.save_extended_header(f)

            checksum = ESPLoader.ESP_CHECKSUM_MAGIC

            # split segments into flash-mapped vs ram-loaded, and take copies so we can mutate them
            flash_segments = [copy.deepcopy(s) for s in sorted(self.segments, key=lambda s:s.addr) if self.is_flash_addr(s.addr)]
            ram_segments = [copy.deepcopy(s) for s in sorted(self.segments, key=lambda s:s.addr) if not self.is_flash_addr(s.addr)]

            # check for multiple ELF sections that are mapped in the same flash mapping region.
            # this is usually a sign of a broken linker script, but if you have a legitimate
            # use case then let us know (we can merge segments here, but as a rule you probably
            # want to merge them in your linker script.)
            if len(flash_segments) > 0:
                last_addr = flash_segments[0].addr
                for segment in flash_segments[1:]:
                    if segment.addr // self.IROM_ALIGN == last_addr // self.IROM_ALIGN:
                        raise FatalError(("Segment loaded at 0x%08x lands in same 64KB flash mapping as segment loaded at 0x%08x. " +
                                          "Can't generate binary. Suggest changing linker script or ELF to merge sections.") %
                                         (segment.addr, last_addr))
                    last_addr = segment.addr

            def get_alignment_data_needed(segment):
                # Actual alignment (in data bytes) required for a segment header: positioned so that
                # after we write the next 8 byte header, file_offs % IROM_ALIGN == segment.addr % IROM_ALIGN
                #
                # (this is because the segment's vaddr may not be IROM_ALIGNed, more likely is aligned
                # IROM_ALIGN+0x18 to account for the binary file header
                align_past = (segment.addr % self.IROM_ALIGN) - self.SEG_HEADER_LEN
                pad_len = (self.IROM_ALIGN - (f.tell() % self.IROM_ALIGN)) + align_past
                if pad_len == 0 or pad_len == self.IROM_ALIGN:
                    return 0  # already aligned

                # subtract SEG_HEADER_LEN a second time, as the padding block has a header as well
                pad_len -= self.SEG_HEADER_LEN
                if pad_len < 0:
                    pad_len += self.IROM_ALIGN
                return pad_len

            # try to fit each flash segment on a 64kB aligned boundary
            # by padding with parts of the non-flash segments...
            while len(flash_segments) > 0:
                segment = flash_segments[0]
                pad_len = get_alignment_data_needed(segment)
                if pad_len > 0:  # need to pad
                    if len(ram_segments) > 0 and pad_len > self.SEG_HEADER_LEN:
                        pad_segment = ram_segments[0].split_image(pad_len)
                        if len(ram_segments[0].data) == 0:
                            ram_segments.pop(0)
                    else:
                        pad_segment = ImageSegment(0, b'\x00' * pad_len, f.tell())
                    checksum = self.save_segment(f, pad_segment, checksum)
                    total_segments += 1
                else:
                    # write the flash segment
                    assert (f.tell() + 8) % self.IROM_ALIGN == segment.addr % self.IROM_ALIGN
                    checksum = self.save_flash_segment(f, segment, checksum)
                    flash_segments.pop(0)
                    total_segments += 1

            # flash segments all written, so write any remaining RAM segments
            for segment in ram_segments:
                checksum = self.save_segment(f, segment, checksum)
                total_segments += 1

            if self.secure_pad:
                # pad the image so that after signing it will end on a a 64KB boundary.
                # This ensures all mapped flash content will be verified.
                if not self.append_digest:
                    raise FatalError("secure_pad only applies if a SHA-256 digest is also appended to the image")
                align_past = (f.tell() + self.SEG_HEADER_LEN) % self.IROM_ALIGN
                # 16 byte aligned checksum (force the alignment to simplify calculations)
                checksum_space = 16
                if self.secure_pad == '1':
                    # after checksum: SHA-256 digest + (to be added by signing process) version, signature + 12 trailing bytes due to alignment
                    space_after_checksum = 32 + 4 + 64 + 12
                elif self.secure_pad == '2':  # Secure Boot V2
                    # after checksum: SHA-256 digest + signature sector, but we place signature sector after the 64KB boundary
                    space_after_checksum = 32
                pad_len = (self.IROM_ALIGN - align_past - checksum_space - space_after_checksum) % self.IROM_ALIGN
                pad_segment = ImageSegment(0, b'\x00' * pad_len, f.tell())

                checksum = self.save_segment(f, pad_segment, checksum)
                total_segments += 1

            # done writing segments
            self.append_checksum(f, checksum)
            image_length = f.tell()

            if self.secure_pad:
                assert ((image_length + space_after_checksum) % self.IROM_ALIGN) == 0

            # kinda hacky: go back to the initial header and write the new segment count
            # that includes padding segments. This header is not checksummed
            f.seek(1)
            try:
                f.write(chr(total_segments))
            except TypeError:  # Python 3
                f.write(bytes([total_segments]))

            if self.append_digest:
                # calculate the SHA256 of the whole file and append it
                f.seek(0)
                digest = hashlib.sha256()
                digest.update(f.read(image_length))
                f.write(digest.digest())

            with open(filename, 'wb') as real_file:
                real_file.write(f.getvalue())

    def save_flash_segment(self, f, segment, checksum=None):
        """ Save the next segment to the image file, return next checksum value if provided """
        segment_end_pos = f.tell() + len(segment.data) + self.SEG_HEADER_LEN
        segment_len_remainder = segment_end_pos % self.IROM_ALIGN
        if segment_len_remainder < 0x24:
            # Work around a bug in ESP-IDF 2nd stage bootloader, that it didn't map the
            # last MMU page, if an IROM/DROM segment was < 0x24 bytes over the page boundary.
            segment.data += b'\x00' * (0x24 - segment_len_remainder)
        return self.save_segment(f, segment, checksum)

    def load_extended_header(self, load_file):
        def split_byte(n):
            return (n & 0x0F, (n >> 4) & 0x0F)

        fields = list(struct.unpack(self.EXTENDED_HEADER_STRUCT_FMT, load_file.read(16)))

        self.wp_pin = fields[0]

        # SPI pin drive stengths are two per byte
        self.clk_drv, self.q_drv = split_byte(fields[1])
        self.d_drv, self.cs_drv = split_byte(fields[2])
        self.hd_drv, self.wp_drv = split_byte(fields[3])

        chip_id = fields[4]
        if chip_id != self.ROM_LOADER.IMAGE_CHIP_ID:
            kprint(("Unexpected chip id in image. Expected %d but value was %d. " +
                  "Is this image for a different chip model?") % (self.ROM_LOADER.IMAGE_CHIP_ID, chip_id))

        # reserved fields in the middle should all be zero
        if any(f for f in fields[6:-1] if f != 0):
            kprint("Warning: some reserved header fields have non-zero values. This image may be from a newer esptool.py?")

        append_digest = fields[-1]  # last byte is append_digest
        if append_digest in [0, 1]:
            self.append_digest = (append_digest == 1)
        else:
            raise RuntimeError("Invalid value for append_digest field (0x%02x). Should be 0 or 1.", append_digest)

    def save_extended_header(self, save_file):
        def join_byte(ln,hn):
            return (ln & 0x0F) + ((hn & 0x0F) << 4)

        append_digest = 1 if self.append_digest else 0

        fields = [self.wp_pin,
                  join_byte(self.clk_drv, self.q_drv),
                  join_byte(self.d_drv, self.cs_drv),
                  join_byte(self.hd_drv, self.wp_drv),
                  self.ROM_LOADER.IMAGE_CHIP_ID,
                  self.min_rev]
        fields += [0] * 8  # padding
        fields += [append_digest]

        packed = struct.pack(self.EXTENDED_HEADER_STRUCT_FMT, *fields)
        save_file.write(packed)


ESP32ROM.BOOTLOADER_IMAGE = ESP32FirmwareImage


class ESP32S2FirmwareImage(ESP32FirmwareImage):
    """ ESP32S2 Firmware Image almost exactly the same as ESP32FirmwareImage """
    ROM_LOADER = ESP32S2ROM


ESP32S2ROM.BOOTLOADER_IMAGE = ESP32S2FirmwareImage


class ELFFile(object):
    SEC_TYPE_PROGBITS = 0x01
    SEC_TYPE_STRTAB = 0x03

    LEN_SEC_HEADER = 0x28

    def __init__(self, name):
        # Load sections from the ELF file
        self.name = name
        with open(self.name, 'rb') as f:
            self._read_elf_file(f)

    def get_section(self, section_name):
        for s in self.sections:
            if s.name == section_name:
                return s
        raise ValueError("No section %s in ELF file" % section_name)

    def _read_elf_file(self, f):
        # read the ELF file header
        LEN_FILE_HEADER = 0x34
        try:
            (ident,_type,machine,_version,
             self.entrypoint,_phoff,shoff,_flags,
             _ehsize, _phentsize,_phnum, shentsize,
             shnum,shstrndx) = struct.unpack("<16sHHLLLLLHHHHHH", f.read(LEN_FILE_HEADER))
        except struct.error as e:
            raise FatalError("Failed to read a valid ELF header from %s: %s" % (self.name, e))

        if byte(ident, 0) != 0x7f or ident[1:4] != b'ELF':
            raise FatalError("%s has invalid ELF magic header" % self.name)
        if machine != 0x5e:
            raise FatalError("%s does not appear to be an Xtensa ELF file. e_machine=%04x" % (self.name, machine))
        if shentsize != self.LEN_SEC_HEADER:
            raise FatalError("%s has unexpected section header entry size 0x%x (not 0x28)" % (self.name, shentsize, self.LEN_SEC_HEADER))
        if shnum == 0:
            raise FatalError("%s has 0 section headers" % (self.name))
        self._read_sections(f, shoff, shnum, shstrndx)

    def _read_sections(self, f, section_header_offs, section_header_count, shstrndx):
        f.seek(section_header_offs)
        len_bytes = section_header_count * self.LEN_SEC_HEADER
        section_header = f.read(len_bytes)
        if len(section_header) == 0:
            raise FatalError("No section header found at offset %04x in ELF file." % section_header_offs)
        if len(section_header) != (len_bytes):
            raise FatalError("Only read 0x%x bytes from section header (expected 0x%x.) Truncated ELF file?" % (len(section_header), len_bytes))

        # walk through the section header and extract all sections
        section_header_offsets = range(0, len(section_header), self.LEN_SEC_HEADER)

        def read_section_header(offs):
            name_offs,sec_type,_flags,lma,sec_offs,size = struct.unpack_from("<LLLLLL", section_header[offs:])
            return (name_offs, sec_type, lma, size, sec_offs)
        all_sections = [read_section_header(offs) for offs in section_header_offsets]
        prog_sections = [s for s in all_sections if s[1] == ELFFile.SEC_TYPE_PROGBITS]

        # search for the string table section
        if not (shstrndx * self.LEN_SEC_HEADER) in section_header_offsets:
            raise FatalError("ELF file has no STRTAB section at shstrndx %d" % shstrndx)
        _,sec_type,_,sec_size,sec_offs = read_section_header(shstrndx * self.LEN_SEC_HEADER)
        if sec_type != ELFFile.SEC_TYPE_STRTAB:
            kprint('WARNING: ELF file has incorrect STRTAB section type 0x%02x' % sec_type)
        f.seek(sec_offs)
        string_table = f.read(sec_size)

        # build the real list of ELFSections by reading the actual section names from the
        # string table section, and actual data for each section from the ELF file itself
        def lookup_string(offs):
            raw = string_table[offs:]
            return raw[:raw.index(b'\x00')]

        def read_data(offs,size):
            f.seek(offs)
            return f.read(size)

        prog_sections = [ELFSection(lookup_string(n_offs), lma, read_data(offs, size)) for (n_offs, _type, lma, size, offs) in prog_sections
                         if lma != 0 and size > 0]
        self.sections = prog_sections

    def sha256(self):
        # return SHA256 hash of the input ELF file
        sha256 = hashlib.sha256()
        with open(self.name, 'rb') as f:
            sha256.update(f.read())
        return sha256.digest()


def slip_reader(port, trace_function):
    """Generator to read SLIP packets from a serial port.
    Yields one full SLIP packet at a time, raises exception on timeout or invalid data.

    Designed to avoid too many calls to serial.read(1), which can bog
    down on slow systems.
    """
    partial_packet = None
    in_escape = False
    while True:
        waiting = port.inWaiting()
        read_bytes = port.read(1 if waiting == 0 else waiting)
        if read_bytes == b'':
            waiting_for = "header" if partial_packet is None else "content"
            trace_function("Timed out waiting for packet %s", waiting_for)
            raise FatalError("Timed out waiting for packet %s" % waiting_for)
        trace_function("Read %d bytes: %s", len(read_bytes), HexFormatter(read_bytes))
        for b in read_bytes:
            if type(b) is int:
                b = bytes([b])  # python 2/3 compat

            if partial_packet is None:  # waiting for packet header
                if b == b'\xc0':
                    partial_packet = b""
                else:
                    trace_function("Read invalid data: %s", HexFormatter(read_bytes))
                    trace_function("Remaining data in serial buffer: %s", HexFormatter(port.read(port.inWaiting())))
                    raise FatalError('Invalid head of packet (0x%s)' % hexify(b))
            elif in_escape:  # part-way through escape sequence
                in_escape = False
                if b == b'\xdc':
                    partial_packet += b'\xc0'
                elif b == b'\xdd':
                    partial_packet += b'\xdb'
                else:
                    trace_function("Read invalid data: %s", HexFormatter(read_bytes))
                    trace_function("Remaining data in serial buffer: %s", HexFormatter(port.read(port.inWaiting())))
                    raise FatalError('Invalid SLIP escape (0xdb, 0x%s)' % (hexify(b)))
            elif b == b'\xdb':  # start of escape sequence
                in_escape = True
            elif b == b'\xc0':  # end of packet
                trace_function("Received full packet: %s", HexFormatter(partial_packet))
                yield partial_packet
                partial_packet = None
            else:  # normal byte in packet
                partial_packet += b


def arg_auto_int(x):
    return int(x, 0)


def div_roundup(a, b):
    """ Return a/b rounded up to nearest integer,
    equivalent result to int(math.ceil(float(int(a)) / float(int(b))), only
    without possible floating point accuracy errors.
    """
    return (int(a) + int(b) - 1) // int(b)


def align_file_position(f, size):
    """ Align the position in the file to the next block of specified size """
    align = (size - 1) - (f.tell() % size)
    f.seek(align, 1)


def flash_size_bytes(size):
    """ Given a flash size of the type passed in args.flash_size
    (ie 512KB or 1MB) then return the size in bytes.
    """
    if "MB" in size:
        return int(size[:size.index("MB")]) * 1024 * 1024
    elif "KB" in size:
        return int(size[:size.index("KB")]) * 1024
    else:
        raise FatalError("Unknown size %s" % size)


def hexify(s, uppercase=True):
    format_str = '%02X' if uppercase else '%02x'
    if not PYTHON2:
        return ''.join(format_str % c for c in s)
    else:
        return ''.join(format_str % ord(c) for c in s)


class HexFormatter(object):
    """
    Wrapper class which takes binary data in its constructor
    and returns a hex string as it's __str__ method.

    This is intended for "lazy formatting" of trace() output
    in hex format. Avoids overhead (significant on slow computers)
    of generating long hex strings even if tracing is disabled.

    Note that this doesn't save any overhead if passed as an
    argument to "%", only when passed to trace()

    If auto_split is set (default), any long line (> 16 bytes) will be
    kprinted as separately indented lines, with ASCII decoding at the end
    of each line.
    """
    def __init__(self, binary_string, auto_split=True):
        self._s = binary_string
        self._auto_split = auto_split

    def __str__(self):
        if self._auto_split and len(self._s) > 16:
            result = ""
            s = self._s
            while len(s) > 0:
                line = s[:16]
                ascii_line = "".join(c if (c == ' ' or (c in string.printable and c not in string.whitespace))
                                     else '.' for c in line.decode('ascii', 'replace'))
                s = s[16:]
                result += "\n    %-16s %-16s | %s" % (hexify(line[:8], False), hexify(line[8:], False), ascii_line)
            return result
        else:
            return hexify(self._s, False)


def pad_to(data, alignment, pad_character=b'\xFF'):
    """ Pad to the next alignment boundary """
    pad_mod = len(data) % alignment
    if pad_mod != 0:
        data += pad_character * (alignment - pad_mod)
    return data


class FatalError(RuntimeError):
    """
    Wrapper class for runtime errors that aren't caused by internal bugs, but by
    ESP8266 responses or input content.
    """
    def __init__(self, message):
        RuntimeError.__init__(self, message)

    @staticmethod
    def WithResult(message, result):
        """
        Return a fatal error object that appends the hex values of
        'result' as a string formatted argument.
        """
        message += " (result was %s)" % hexify(result)
        return FatalError(message)


class NotImplementedInROMError(FatalError):
    """
    Wrapper class for the error thrown when a particular ESP bootloader function
    is not implemented in the ROM bootloader.
    """
    def __init__(self, bootloader, func):
        FatalError.__init__(self, "%s ROM does not support function %s." % (bootloader.CHIP_NAME, func.__name__))


class NotSupportedError(FatalError):
    def __init__(self, esp, function_name):
        FatalError.__init__(self, "Function %s is not supported for %s." % (function_name, esp.CHIP_NAME))

# "Operation" commands, executable at command line. One function each
#
# Each function takes either two args (<ESPLoader instance>, <args>) or a single <args>
# argument.


class UnsupportedCommandError(FatalError):
    """
    Wrapper class for when ROM loader returns an invalid command response.

Usually this indicates the loader is running in a reduced mode.
    """
    def __init__(self):
        FatalError.__init__(self, "Invalid (unsupported) command")


def load_ram(esp, args):
    image = LoadFirmwareImage(esp.CHIP_NAME, args.filename)

    kprint('RAM boot...')
    for seg in image.segments:
        size = len(seg.data)
        kprint('Downloading %d bytes at %08x...' % (size, seg.addr), end=' ')
        
        esp.mem_begin(size, div_roundup(size, esp.ESP_RAM_BLOCK), esp.ESP_RAM_BLOCK, seg.addr)

        seq = 0
        while len(seg.data) > 0:
            esp.mem_block(seg.data[0:esp.ESP_RAM_BLOCK], seq)
            seg.data = seg.data[esp.ESP_RAM_BLOCK:]
            seq += 1
        kprint('done!')

    kprint('All segments done, executing at %08x' % image.entrypoint)
    esp.mem_finish(image.entrypoint)


def read_mem(esp, args):
    kprint('0x%08x = 0x%08x' % (args.address, esp.read_reg(args.address)))


def write_mem(esp, args):
    esp.write_reg(args.address, args.value, args.mask, 0)
    kprint('Wrote %08x, mask %08x to %08x' % (args.value, args.mask, args.address))


def dump_mem(esp, args):
    with open(args.filename, 'wb') as f:
        for i in range(args.size // 4):
            d = esp.read_reg(args.address + (i * 4))
            f.write(struct.pack(b'<I', d))
            if f.tell() % 1024 == 0:
                kprint_overwrite('%d bytes read... (%d %%)' % (f.tell(),
                                                              f.tell() * 100 // args.size))
            
    kprint_overwrite("Read %d bytes" % f.tell(), last_line=True)
    kprint('Done!')


def detect_flash_size(esp, args):
    if args.flash_size == 'detect':
        flash_id = esp.flash_id()
        size_id = flash_id >> 16
        args.flash_size = DETECTED_FLASH_SIZES.get(size_id)
        if args.flash_size is None:
            kprint('Warning: Could not auto-detect Flash size (FlashID=0x%x, SizeID=0x%x), defaulting to 4MB' % (flash_id, size_id))
            args.flash_size = '4MB'
        else:
            kprint('Auto-detected Flash size:', args.flash_size)


def _update_image_flash_params(esp, address, args, image):
    """ Modify the flash mode & size bytes if this looks like an executable bootloader image  """
    if len(image) < 8:
        return image  # not long enough to be a bootloader image

    # unpack the (potential) image header
    magic, _, flash_mode, flash_size_freq = struct.unpack("BBBB", image[:4])
    if address != esp.BOOTLOADER_FLASH_OFFSET:
        return image  # not flashing bootloader offset, so don't modify this

    if (args.flash_mode, args.flash_freq, args.flash_size) == ('keep',) * 3:
        return image  # all settings are 'keep', not modifying anything

    # easy check if this is an image: does it start with a magic byte?
    if magic != esp.ESP_IMAGE_MAGIC:
        kprint("Warning: Image file at 0x%x doesn't look like an image file, so not changing any flash settings." % address)
        return image

    # make sure this really is an image, and not just data that
    # starts with esp.ESP_IMAGE_MAGIC (mostly a problem for encrypted
    # images that happen to start with a magic byte
    try:
        test_image = esp.BOOTLOADER_IMAGE(io.BytesIO(image))
        test_image.verify()
    except Exception:
        kprint("Warning: Image file at 0x%x is not a valid %s image, so not changing any flash settings." % (address,esp.CHIP_NAME))
        return image

    if args.flash_mode != 'keep':
        flash_mode = {'qio':0, 'qout':1, 'dio':2, 'dout': 3}[args.flash_mode]

    flash_freq = flash_size_freq & 0x0F
    if args.flash_freq != 'keep':
        flash_freq = {'40m':0, '26m':1, '20m':2, '80m': 0xf}[args.flash_freq]

    flash_size = flash_size_freq & 0xF0
    if args.flash_size != 'keep':
        flash_size = esp.parse_flash_size_arg(args.flash_size)

    flash_params = struct.pack(b'BB', flash_mode, flash_size + flash_freq)
    if flash_params != image[2:4]:
        kprint('Flash params set to 0x%04x' % struct.unpack(">H", flash_params))
        image = image[0:2] + flash_params + image[4:]
    return image


def write_flash(esp, args):
    # set args.compress based on default behaviour:
    # -> if either --compress or --no-compress is set, honour that
    # -> otherwise, set --compress unless --no-stub is set
    if args.compress is None and not args.no_compress:
        args.compress = not args.no_stub

    # For encrypt option we do few sanity checks before actual flash write
    if args.encrypt:
        do_write = True

        if esp.get_encrypted_download_disabled():
            raise FatalError("This chip has encrypt functionality in UART download mode disabled. "
                             + "This is the Flash Encryption configuration for Production mode instead of Development mode.")

        crypt_cfg_efuse = esp.get_flash_crypt_config()

        if crypt_cfg_efuse is not None and crypt_cfg_efuse != 0xF:
            kprint('Unexpected FLASH_CRYPT_CONFIG value: 0x%x' % (crypt_cfg_efuse))
            do_write = False

        enc_key_valid = esp.is_flash_encryption_key_valid()

        if not enc_key_valid:
            kprint('Flash encryption key is not programmed')
            do_write = False

        for address, argfile in args.addr_filename:
            if address % esp.FLASH_ENCRYPTED_WRITE_ALIGN:
                kprint("File %s address 0x%x is not %d byte aligned, can't flash encrypted" %
                      (argfile.name, address, esp.FLASH_ENCRYPTED_WRITE_ALIGN))
                do_write = False

        if not do_write and not args.ignore_flash_encryption_efuse_setting:
            raise FatalError("Can't perform encrypted flash write, consult Flash Encryption documentation for more information")

    # verify file sizes fit in flash
    if args.flash_size != 'keep':  # TODO: check this even with 'keep'
        flash_end = flash_size_bytes(args.flash_size)
        for address, argfile in args.addr_filename:
            argfile.seek(0,2)  # seek to end
            if address + argfile.tell() > flash_end:
                raise FatalError(("File %s (length %d) at offset %d will not fit in %d bytes of flash. " +
                                  "Use --flash-size argument, or change flashing address.")
                                 % (argfile.name, argfile.tell(), address, flash_end))
            argfile.seek(0)

    if args.erase_all:
        erase_flash(esp, args)

    if args.encrypt and args.compress:
        kprint('\nWARNING: - compress and encrypt options are mutually exclusive ')
        kprint('Will flash uncompressed')
        args.compress = False

    for address, argfile in args.addr_filename:
        if args.no_stub:
            kprint('Erasing flash...')
        image = pad_to(argfile.read(), esp.FLASH_ENCRYPTED_WRITE_ALIGN if args.encrypt else 4)
        if len(image) == 0:
            kprint('WARNING: File %s is empty' % argfile.name)
            continue
        image = _update_image_flash_params(esp, address, args, image)
        calcmd5 = hashlib.md5(image).hexdigest()
        uncsize = len(image)
        if args.compress:
            uncimage = image
            image = zlib.compress(uncimage, 9)
            ratio = uncsize / len(image)
            blocks = esp.flash_defl_begin(uncsize, len(image), address)
        else:
            ratio = 1.0
            blocks = esp.flash_begin(uncsize, address)
        argfile.seek(0)  # in case we need it again
        seq = 0
        written = 0
        t = time.time()
        while len(image) > 0:
            kprint_overwrite('Writing at 0x%08x... (%d %%)' % (address + seq * esp.FLASH_WRITE_SIZE, 100 * (seq + 1) // blocks))
            
            block = image[0:esp.FLASH_WRITE_SIZE]
            if args.compress:
                esp.flash_defl_block(block, seq, timeout=DEFAULT_TIMEOUT * ratio * 2)
            else:
                # Pad the last block
                block = block + b'\xff' * (esp.FLASH_WRITE_SIZE - len(block))
                if args.encrypt:
                    esp.flash_encrypt_block(block, seq)
                else:
                    esp.flash_block(block, seq)
            image = image[esp.FLASH_WRITE_SIZE:]
            seq += 1
            written += len(block)
        t = time.time() - t
        speed_msg = ""
        if args.compress:
            if t > 0.0:
                speed_msg = " (effective %.1f kbit/s)" % (uncsize / t * 8 / 1000)
            kprint_overwrite('Wrote %d bytes (%d compressed) at 0x%08x in %.1f seconds%s...' % (uncsize, written, address, t, speed_msg), last_line=True)
        else:
            if t > 0.0:
                speed_msg = " (%.1f kbit/s)" % (written / t * 8 / 1000)
            kprint_overwrite('Wrote %d bytes at 0x%08x in %.1f seconds%s...' % (written, address, t, speed_msg), last_line=True)

        if not args.encrypt:
            try:
                res = esp.flash_md5sum(address, uncsize)
                if res != calcmd5:
                    kprint('File  md5: %s' % calcmd5)
                    kprint('Flash md5: %s' % res)
                    kprint('MD5 of 0xFF is %s' % (hashlib.md5(b'\xFF' * uncsize).hexdigest()))
                    raise FatalError("MD5 of file does not match data in flash!")
                else:
                    kprint('Hash of data verified.')
            except NotImplementedInROMError:
                pass

    kprint('\nLeaving...')

    if esp.IS_STUB:
        # skip sending flash_finish to ROM loader here,
        # as it causes the loader to exit and run user code
        esp.flash_begin(0, 0)
        if args.compress:
            esp.flash_defl_finish(False)
        else:
            esp.flash_finish(False)

    if args.verify:
        kprint('Verifying just-written flash...')
        kprint('(This option is deprecated, flash contents are now always read back after flashing.)')
        verify_flash(esp, args)


def image_info(args):
    image = LoadFirmwareImage(args.chip, args.filename)
    kprint('Image version: %d' % image.version)
    kprint('Entry point: %08x' % image.entrypoint if image.entrypoint != 0 else 'Entry point not set')
    kprint('%d segments' % len(image.segments))
    kprint()
    idx = 0
    for seg in image.segments:
        idx += 1
        seg_name = ", ".join([seg_range[2] for seg_range in image.ROM_LOADER.MEMORY_MAP if seg_range[0] <= seg.addr < seg_range[1]])
        kprint('Segment %d: %r [%s]' % (idx, seg, seg_name))
    calc_checksum = image.calculate_checksum()
    kprint('Checksum: %02x (%s)' % (image.checksum,
                                   'valid' if image.checksum == calc_checksum else 'invalid - calculated %02x' % calc_checksum))
    try:
        digest_msg = 'Not appended'
        if image.append_digest:
            is_valid = image.stored_digest == image.calc_digest
            digest_msg = "%s (%s)" % (hexify(image.calc_digest).lower(),
                                      "valid" if is_valid else "invalid")
            kprint('Validation Hash: %s' % digest_msg)
    except AttributeError:
        pass  # ESP8266 image has no append_digest field


def make_image(args):
    image = ESP8266ROMFirmwareImage()
    if len(args.segfile) == 0:
        raise FatalError('No segments specified')
    if len(args.segfile) != len(args.segaddr):
        raise FatalError('Number of specified files does not match number of specified addresses')
    for (seg, addr) in zip(args.segfile, args.segaddr):
        with open(seg, 'rb') as f:
            data = f.read()
            image.segments.append(ImageSegment(addr, data))
    image.entrypoint = args.entrypoint
    image.save(args.output)


def elf2image(args):
    e = ELFFile(args.input)
    if args.chip == 'auto':  # Default to ESP8266 for backwards compatibility
        kprint("Creating image for ESP8266...")
        args.chip = 'esp8266'

    if args.chip == 'esp32':
        image = ESP32FirmwareImage()
        if args.secure_pad:
            image.secure_pad = '1'
        elif args.secure_pad_v2:
            image.secure_pad = '2'
        image.min_rev = int(args.min_rev)
    elif args.chip == 'esp32s2':
        image = ESP32S2FirmwareImage()
        if args.secure_pad_v2:
            image.secure_pad = '2'
        image.min_rev = 0
    elif args.version == '1':  # ESP8266
        image = ESP8266ROMFirmwareImage()
    else:
        image = ESP8266V2FirmwareImage()
    image.entrypoint = e.entrypoint
    image.segments = e.sections  # ELFSection is a subclass of ImageSegment
    image.flash_mode = {'qio':0, 'qout':1, 'dio':2, 'dout': 3}[args.flash_mode]
    image.flash_size_freq = image.ROM_LOADER.FLASH_SIZES[args.flash_size]
    image.flash_size_freq += {'40m':0, '26m':1, '20m':2, '80m': 0xf}[args.flash_freq]

    if args.elf_sha256_offset:
        image.elf_sha256 = e.sha256()
        image.elf_sha256_offset = args.elf_sha256_offset

    image.verify()

    if args.output is None:
        args.output = image.default_output_name(args.input)
    image.save(args.output)


def read_mac(esp, args):
    mac = esp.read_mac()

    def kprint_mac(label, mac):
        kprint('%s: %s' % (label, ':'.join(map(lambda x: '%02x' % x, mac))))
    kprint_mac("MAC", mac)


def chip_id(esp, args):
    try:
        chipid = esp.chip_id()
        kprint('Chip ID: 0x%08x' % chipid)
    except NotSupportedError:
        kprint('Warning: %s has no Chip ID. Reading MAC instead.' % esp.CHIP_NAME)
        read_mac(esp, args)


def erase_flash(esp, args):
    kprint('Erasing flash (this may take a while)...')
    t = time.time()
    esp.erase_flash()
    kprint('Chip erase completed successfully in %.1fs' % (time.time() - t))


def erase_region(esp, args):
    kprint('Erasing region (may be slow depending on size)...')
    t = time.time()
    esp.erase_region(args.address, args.size)
    kprint('Erase completed successfully in %.1f seconds.' % (time.time() - t))


def run(esp, args):
    esp.run()


def flash_id(esp, args):
    flash_id = esp.flash_id()
    kprint('Manufacturer: %02x' % (flash_id & 0xff))
    flid_lowbyte = (flash_id >> 16) & 0xFF
    kprint('Device: %02x%02x' % ((flash_id >> 8) & 0xff, flid_lowbyte))
    kprint('Detected flash size: %s' % (DETECTED_FLASH_SIZES.get(flid_lowbyte, "Unknown")))


def read_flash(esp, args):
    if args.no_progress:
        flash_progress = None
    else:
        def flash_progress(progress, length):
            msg = '%d (%d %%)' % (progress, progress * 100.0 / length)
            padding = '\b' * len(msg)
            if progress == length:
                padding = '\n'
            kprint(msg + padding)
            
    t = time.time()
    data = esp.read_flash(args.address, args.size, flash_progress)
    t = time.time() - t
    kprint_overwrite('Read %d bytes at 0x%x in %.1f seconds (%.1f kbit/s)...'
                    % (len(data), args.address, t, len(data) / t * 8 / 1000), last_line=True)
    with open(args.filename, 'wb') as f:
        f.write(data)


def verify_flash(esp, args):
    differences = False

    for address, argfile in args.addr_filename:
        image = pad_to(argfile.read(), 4)
        argfile.seek(0)  # rewind in case we need it again

        image = _update_image_flash_params(esp, address, args, image)

        image_size = len(image)
        kprint('Verifying 0x%x (%d) bytes @ 0x%08x in flash against %s...' % (image_size, image_size, address, argfile.name))
        # Try digest first, only read if there are differences.
        digest = esp.flash_md5sum(address, image_size)
        expected_digest = hashlib.md5(image).hexdigest()
        if digest == expected_digest:
            kprint('-- verify OK (digest matched)')
            continue
        else:
            differences = True
            if getattr(args, 'diff', 'no') != 'yes':
                kprint('-- verify FAILED (digest mismatch)')
                continue

        flash = esp.read_flash(address, image_size)
        assert flash != image
        diff = [i for i in range(image_size) if flash[i] != image[i]]
        kprint('-- verify FAILED: %d differences, first @ 0x%08x' % (len(diff), address + diff[0]))
        for d in diff:
            flash_byte = flash[d]
            image_byte = image[d]
            if PYTHON2:
                flash_byte = ord(flash_byte)
                image_byte = ord(image_byte)
            kprint('   %08x %02x %02x' % (address + d, flash_byte, image_byte))
    if differences:
        raise FatalError("Verify failed.")


def read_flash_status(esp, args):
    kprint('Status value: 0x%04x' % esp.read_status(args.bytes))


def write_flash_status(esp, args):
    fmt = "0x%%0%dx" % (args.bytes * 2)
    args.value = args.value & ((1 << (args.bytes * 8)) - 1)
    kprint(('Initial flash status: ' + fmt) % esp.read_status(args.bytes))
    kprint(('Setting flash status: ' + fmt) % args.value)
    esp.write_status(args.value, args.bytes, args.non_volatile)
    kprint(('After flash status:   ' + fmt) % esp.read_status(args.bytes))


def get_security_info(esp, args):
    (flags, flash_crypt_cnt, key_purposes) = esp.get_security_info()
    # TODO: better display
    kprint('Flags: 0x%08x (%s)' % (flags, bin(flags)))
    kprint('Flash_Crypt_Cnt: 0x%x' % flash_crypt_cnt)
    kprint('Key_Purposes: %s' % (key_purposes,))


def version(args):
    kprint(__version__)

#
# End of operations functions
#


def main(custom_commandline=None, handler=None, cdcPort=None):
    """
    Main function for esptool

    custom_commandline - Optional override for default arguments parsing (that uses sys.argv), can be a list of custom arguments
    as strings. Arguments and their values need to be added as individual items to the list e.g. "-b 115200" thus
    becomes ['-b', '115200'].
    """
    global kprint, cdc
    if handler:
        kprint = handler
    if cdcPort:
        cdc = cdcPort

    parser = argparse.ArgumentParser(description='esptool.py v%s - ESP8266 ROM Bootloader Utility' % __version__, prog='esptool')

    parser.add_argument('--chip', '-c',
                        help='Target chip type',
                        type=lambda c: c.lower().replace('-', ''),  # support ESP32-S2, etc.
                        choices=['auto', 'esp8266', 'esp32', 'esp32s2'],
                        default=os.environ.get('ESPTOOL_CHIP', 'auto'))

    parser.add_argument(
        '--port', '-p',
        help='Serial port device',
        default=os.environ.get('ESPTOOL_PORT', None))

    parser.add_argument(
        '--baud', '-b',
        help='Serial port baud rate used when flashing/reading',
        type=arg_auto_int,
        default=os.environ.get('ESPTOOL_BAUD', ESPLoader.ESP_ROM_BAUD))

    parser.add_argument(
        '--before',
        help='What to do before connecting to the chip',
        choices=['default_reset', 'no_reset', 'no_reset_no_sync'],
        default=os.environ.get('ESPTOOL_BEFORE', 'default_reset'))

    parser.add_argument(
        '--after', '-a',
        help='What to do after esptool.py is finished',
        choices=['hard_reset', 'soft_reset', 'no_reset'],
        default=os.environ.get('ESPTOOL_AFTER', 'hard_reset'))

    parser.add_argument(
        '--no-stub',
        help="Disable launching the flasher stub, only talk to ROM bootloader. Some features will not be available.",
        action='store_true')

    parser.add_argument(
        '--trace', '-t',
        help="Enable trace-level output of esptool.py interactions.",
        action='store_true')

    parser.add_argument(
        '--override-vddsdio',
        help="Override ESP32 VDDSDIO internal voltage regulator (use with care)",
        choices=ESP32ROM.OVERRIDE_VDDSDIO_CHOICES,
        nargs='?')

    parser.add_argument(
        '--connect-attempts',
        help=('Number of attempts to connect, negative or 0 for infinite. '
              'Default: %d.' % DEFAULT_CONNECT_ATTEMPTS),
        type=int,
        default=os.environ.get('ESPTOOL_CONNECT_ATTEMPTS', DEFAULT_CONNECT_ATTEMPTS))

    subparsers = parser.add_subparsers(
        dest='operation',
        help='Run esptool {command} -h for additional help')

    def add_spi_connection_arg(parent):
        parent.add_argument('--spi-connection', '-sc', help='ESP32-only argument. Override default SPI Flash connection. ' +
                            'Value can be SPI, HSPI or a comma-separated list of 5 I/O numbers to use for SPI flash (CLK,Q,D,HD,CS).',
                            action=SpiConnectionAction)
    # riven, add libusb support for esptool
    # parser_cdc = subparsers.add_parser(
    #     'cdc',
    #     help='CDC port instance')
    # parser_cdc.add_argument('cdc', help='CDC instance')

    parser_load_ram = subparsers.add_parser(
        'load_ram',
        help='Download an image to RAM and execute')
    parser_load_ram.add_argument('filename', help='Firmware image')

    parser_dump_mem = subparsers.add_parser(
        'dump_mem',
        help='Dump arbitrary memory to disk')
    parser_dump_mem.add_argument('address', help='Base address', type=arg_auto_int)
    parser_dump_mem.add_argument('size', help='Size of region to dump', type=arg_auto_int)
    parser_dump_mem.add_argument('filename', help='Name of binary dump')

    parser_read_mem = subparsers.add_parser(
        'read_mem',
        help='Read arbitrary memory location')
    parser_read_mem.add_argument('address', help='Address to read', type=arg_auto_int)

    parser_write_mem = subparsers.add_parser(
        'write_mem',
        help='Read-modify-write to arbitrary memory location')
    parser_write_mem.add_argument('address', help='Address to write', type=arg_auto_int)
    parser_write_mem.add_argument('value', help='Value', type=arg_auto_int)
    parser_write_mem.add_argument('mask', help='Mask of bits to write', type=arg_auto_int)

    def add_spi_flash_subparsers(parent, is_elf2image):
        """ Add common parser arguments for SPI flash properties """
        extra_keep_args = [] if is_elf2image else ['keep']
        auto_detect = not is_elf2image

        if auto_detect:
            extra_fs_message = ", detect, or keep"
        else:
            extra_fs_message = ""

        parent.add_argument('--flash_freq', '-ff', help='SPI Flash frequency',
                            choices=extra_keep_args + ['40m', '26m', '20m', '80m'],
                            default=os.environ.get('ESPTOOL_FF', '40m' if is_elf2image else 'keep'))
        parent.add_argument('--flash_mode', '-fm', help='SPI Flash mode',
                            choices=extra_keep_args + ['qio', 'qout', 'dio', 'dout'],
                            default=os.environ.get('ESPTOOL_FM', 'qio' if is_elf2image else 'keep'))
        parent.add_argument('--flash_size', '-fs', help='SPI Flash size in MegaBytes (1MB, 2MB, 4MB, 8MB, 16M)'
                            ' plus ESP8266-only (256KB, 512KB, 2MB-c1, 4MB-c1)' + extra_fs_message,
                            action=FlashSizeAction, auto_detect=auto_detect,
                            default=os.environ.get('ESPTOOL_FS', 'detect' if auto_detect else '1MB'))
        add_spi_connection_arg(parent)

    parser_write_flash = subparsers.add_parser(
        'write_flash',
        help='Write a binary blob to flash')

    parser_write_flash.add_argument('addr_filename', metavar='<address> <filename>', help='Address followed by binary filename, separated by space',
                                    action=AddrFilenamePairAction)
    parser_write_flash.add_argument('--erase-all', '-e',
                                    help='Erase all regions of flash (not just write areas) before programming',
                                    action="store_true")

    add_spi_flash_subparsers(parser_write_flash, is_elf2image=False)
    parser_write_flash.add_argument('--no-progress', '-p', help='Suppress progress output', action="store_true")
    parser_write_flash.add_argument('--verify', help='Verify just-written data on flash ' +
                                    '(mostly superfluous, data is read back during flashing)', action='store_true')
    parser_write_flash.add_argument('--encrypt', help='Apply flash encryption when writing data (required correct efuse settings)',
                                    action='store_true')
    parser_write_flash.add_argument('--ignore-flash-encryption-efuse-setting', help='Ignore flash encryption efuse settings ',
                                    action='store_true')

    compress_args = parser_write_flash.add_mutually_exclusive_group(required=False)
    compress_args.add_argument('--compress', '-z', help='Compress data in transfer (default unless --no-stub is specified)',action="store_true", default=None)
    compress_args.add_argument('--no-compress', '-u', help='Disable data compression during transfer (default if --no-stub is specified)',action="store_true")

    subparsers.add_parser(
        'run',
        help='Run application code in flash')

    parser_image_info = subparsers.add_parser(
        'image_info',
        help='Dump headers from an application image')
    parser_image_info.add_argument('filename', help='Image file to parse')

    parser_make_image = subparsers.add_parser(
        'make_image',
        help='Create an application image from binary files')
    parser_make_image.add_argument('output', help='Output image file')
    parser_make_image.add_argument('--segfile', '-f', action='append', help='Segment input file')
    parser_make_image.add_argument('--segaddr', '-a', action='append', help='Segment base address', type=arg_auto_int)
    parser_make_image.add_argument('--entrypoint', '-e', help='Address of entry point', type=arg_auto_int, default=0)

    parser_elf2image = subparsers.add_parser(
        'elf2image',
        help='Create an application image from ELF file')
    parser_elf2image.add_argument('input', help='Input ELF file')
    parser_elf2image.add_argument('--output', '-o', help='Output filename prefix (for version 1 image), or filename (for version 2 single image)', type=str)
    parser_elf2image.add_argument('--version', '-e', help='Output image version', choices=['1','2'], default='1')
    parser_elf2image.add_argument('--min-rev', '-r', help='Minimum chip revision', choices=['0','1','2','3'], default='0')
    parser_elf2image.add_argument('--secure-pad', action='store_true',
                                  help='Pad image so once signed it will end on a 64KB boundary. For Secure Boot v1 images only.')
    parser_elf2image.add_argument('--secure-pad-v2', action='store_true',
                                  help='Pad image to 64KB, so once signed its signature sector will start at the next 64K block. '
                                  'For Secure Boot v2 images only.')
    parser_elf2image.add_argument('--elf-sha256-offset', help='If set, insert SHA256 hash (32 bytes) of the input ELF file at specified offset in the binary.',
                                  type=arg_auto_int, default=None)

    add_spi_flash_subparsers(parser_elf2image, is_elf2image=True)

    subparsers.add_parser(
        'read_mac',
        help='Read MAC address from OTP ROM')

    subparsers.add_parser(
        'chip_id',
        help='Read Chip ID from OTP ROM')

    parser_flash_id = subparsers.add_parser(
        'flash_id',
        help='Read SPI flash manufacturer and device ID')
    add_spi_connection_arg(parser_flash_id)

    parser_read_status = subparsers.add_parser(
        'read_flash_status',
        help='Read SPI flash status register')

    add_spi_connection_arg(parser_read_status)
    parser_read_status.add_argument('--bytes', help='Number of bytes to read (1-3)', type=int, choices=[1,2,3], default=2)

    parser_write_status = subparsers.add_parser(
        'write_flash_status',
        help='Write SPI flash status register')

    add_spi_connection_arg(parser_write_status)
    parser_write_status.add_argument('--non-volatile', help='Write non-volatile bits (use with caution)', action='store_true')
    parser_write_status.add_argument('--bytes', help='Number of status bytes to write (1-3)', type=int, choices=[1,2,3], default=2)
    parser_write_status.add_argument('value', help='New value', type=arg_auto_int)

    parser_read_flash = subparsers.add_parser(
        'read_flash',
        help='Read SPI flash content')
    add_spi_connection_arg(parser_read_flash)
    parser_read_flash.add_argument('address', help='Start address', type=arg_auto_int)
    parser_read_flash.add_argument('size', help='Size of region to dump', type=arg_auto_int)
    parser_read_flash.add_argument('filename', help='Name of binary dump')
    parser_read_flash.add_argument('--no-progress', '-p', help='Suppress progress output', action="store_true")

    parser_verify_flash = subparsers.add_parser(
        'verify_flash',
        help='Verify a binary blob against flash')
    parser_verify_flash.add_argument('addr_filename', help='Address and binary file to verify there, separated by space',
                                     action=AddrFilenamePairAction)
    parser_verify_flash.add_argument('--diff', '-d', help='Show differences',
                                     choices=['no', 'yes'], default='no')
    add_spi_flash_subparsers(parser_verify_flash, is_elf2image=False)

    parser_erase_flash = subparsers.add_parser(
        'erase_flash',
        help='Perform Chip Erase on SPI flash')
    add_spi_connection_arg(parser_erase_flash)

    parser_erase_region = subparsers.add_parser(
        'erase_region',
        help='Erase a region of the flash')
    add_spi_connection_arg(parser_erase_region)
    parser_erase_region.add_argument('address', help='Start address (must be multiple of 4096)', type=arg_auto_int)
    parser_erase_region.add_argument('size', help='Size of region to erase (must be multiple of 4096)', type=arg_auto_int)

    subparsers.add_parser(
        'version', help='kprint esptool version')

    subparsers.add_parser('get_security_info', help='Get some security-related data')

    # internal sanity check - every operation matches a module function of the same name
    for operation in subparsers.choices.keys():
        assert operation in globals(), "%s should be a module function" % operation

    expand_file_arguments()

    args = parser.parse_args(custom_commandline)

    kprint('esptool.py v%s' % __version__)

    # operation function can take 1 arg (args), 2 args (esp, arg)
    # or be a member function of the ESPLoader class.

    if args.operation is None:
        parser.kprint_help()
        sys.exit(1)

    operation_func = globals()[args.operation]

    if PYTHON2:
        # This function is depreciated in Python3
        operation_args = inspect.getargspec(operation_func).args
    else:
        operation_args = inspect.getfullargspec(operation_func).args
    if operation_args[0] == 'esp':  # operation function takes an ESPLoader connection object
        try:
            if args.before != "no_reset_no_sync":
                initial_baud = min(ESPLoader.ESP_ROM_BAUD, args.baud)  # don't sync faster than the default baud rate
            else:
                initial_baud = args.baud

            if args.port is None:
                ser_list = sorted(ports.device for ports in list_ports.comports())
                kprint("Found %d serial ports" % len(ser_list))
            else:
                ser_list = [args.port]
            esp = None
            for each_port in reversed(ser_list):
                kprint("Serial port %s" % each_port)
                try:
                    if args.chip == 'auto':
                        esp = ESPLoader.detect_chip(each_port, initial_baud, args.before, args.trace,
                                                    args.connect_attempts)
                    else:
                        chip_class = {
                            'esp8266': ESP8266ROM,
                            'esp32': ESP32ROM,
                            'esp32s2': ESP32S2ROM,
                        }[args.chip]
                        esp = chip_class(each_port, initial_baud, args.trace)
                        esp.connect(args.before, args.connect_attempts)
                    break
                except (FatalError, OSError) as err:
                    if args.port is not None:
                        raise
                    kprint("%s failed to connect: %s" % (each_port, err))
                    esp = None
            if esp is None:
                raise FatalError("Could not connect to an Espressif device on any of the %d available serial ports." % len(ser_list))

            kprint("Chip is %s" % (esp.get_chip_description()))

            kprint("Features: %s" % ", ".join(esp.get_chip_features()))

            kprint("Crystal is %dMHz" % esp.get_crystal_freq())

            read_mac(esp, args)

            if not args.no_stub:
                esp = esp.run_stub()

            if args.override_vddsdio:
                esp.override_vddsdio(args.override_vddsdio)

            if args.baud > initial_baud:
                try:
                    esp.change_baud(args.baud)
                except NotImplementedInROMError:
                    kprint("WARNING: ROM doesn't support changing baud rate. Keeping initial baud rate %d" % initial_baud)

            # override common SPI flash parameter stuff if configured to do so
            if hasattr(args, "spi_connection") and args.spi_connection is not None:
                if esp.CHIP_NAME != "ESP32":
                    raise FatalError("Chip %s does not support --spi-connection option." % esp.CHIP_NAME)
                kprint("Configuring SPI flash mode...")
                esp.flash_spi_attach(args.spi_connection)
            elif args.no_stub:
                kprint("Enabling default SPI flash mode...")
                # ROM loader doesn't enable flash unless we explicitly do it
                esp.flash_spi_attach(0)

            if hasattr(args, "flash_size"):
                kprint("Configuring flash size...")
                detect_flash_size(esp, args)
                if args.flash_size != 'keep':  # TODO: should set this even with 'keep'
                    esp.flash_set_parameters(flash_size_bytes(args.flash_size))

            try:
                operation_func(esp, args)
            finally:
                try:  # Clean up AddrFilenamePairAction files
                    for address, argfile in args.addr_filename:
                        argfile.close()
                except AttributeError:
                    pass

            # Handle post-operation behaviour (reset or other)
            if operation_func == load_ram:
                # the ESP is now running the loaded image, so let it run
                kprint('Exiting immediately.')
            elif args.after == 'hard_reset':
                kprint('Hard resetting via RTS pin...')
                esp.hard_reset()
            elif args.after == 'soft_reset':
                kprint('Soft resetting...')
                # flash_finish will trigger a soft reset
                esp.soft_reset(False)
            else:
                kprint('Staying in bootloader.')
                if esp.IS_STUB:
                    esp.soft_reset(True)  # exit stub back to ROM loader
        finally:
            esp._port.close()

    else:
        operation_func(args)


def expand_file_arguments():
    """ Any argument starting with "@" gets replaced with all values read from a text file.
    Text file arguments can be split by newline or by space.
    Values are added "as-is", as if they were specified in this order on the command line.
    """
    new_args = []
    expanded = False
    for arg in sys.argv:
        if arg.startswith("@"):
            expanded = True
            with open(arg[1:],"r") as f:
                for line in f.readlines():
                    new_args += shlex.split(line)
        else:
            new_args.append(arg)
    if expanded:
        kprint("esptool.py %s" % (" ".join(new_args[1:])))
        sys.argv = new_args


class FlashSizeAction(argparse.Action):
    """ Custom flash size parser class to support backwards compatibility with megabit size arguments.

    (At next major relase, remove deprecated sizes and this can become a 'normal' choices= argument again.)
    """
    def __init__(self, option_strings, dest, nargs=1, auto_detect=False, **kwargs):
        super(FlashSizeAction, self).__init__(option_strings, dest, nargs, **kwargs)
        self._auto_detect = auto_detect

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            value = {
                '2m': '256KB',
                '4m': '512KB',
                '8m': '1MB',
                '16m': '2MB',
                '32m': '4MB',
                '16m-c1': '2MB-c1',
                '32m-c1': '4MB-c1',
            }[values[0]]
            kprint("WARNING: Flash size arguments in megabits like '%s' are deprecated." % (values[0]))
            kprint("Please use the equivalent size '%s'." % (value))
            kprint("Megabit arguments may be removed in a future release.")
        except KeyError:
            value = values[0]

        known_sizes = dict(ESP8266ROM.FLASH_SIZES)
        known_sizes.update(ESP32ROM.FLASH_SIZES)
        if self._auto_detect:
            known_sizes['detect'] = 'detect'
            known_sizes['keep'] = 'keep'
        if value not in known_sizes:
            raise argparse.ArgumentError(self, '%s is not a known flash size. Known sizes: %s' % (value, ", ".join(known_sizes.keys())))
        setattr(namespace, self.dest, value)


class SpiConnectionAction(argparse.Action):
    """ Custom action to parse 'spi connection' override. Values are SPI, HSPI, or a sequence of 5 pin numbers separated by commas.
    """
    def __call__(self, parser, namespace, value, option_string=None):
        if value.upper() == "SPI":
            value = 0
        elif value.upper() == "HSPI":
            value = 1
        elif "," in value:
            values = value.split(",")
            if len(values) != 5:
                raise argparse.ArgumentError(self, '%s is not a valid list of comma-separate pin numbers. Must be 5 numbers - CLK,Q,D,HD,CS.' % value)
            try:
                values = tuple(int(v,0) for v in values)
            except ValueError:
                raise argparse.ArgumentError(self, '%s is not a valid argument. All pins must be numeric values' % values)
            if any([v for v in values if v > 33 or v < 0]):
                raise argparse.ArgumentError(self, 'Pin numbers must be in the range 0-33.')
            # encode the pin numbers as a 32-bit integer with packed 6-bit values, the same way ESP32 ROM takes them
            # TODO: make this less ESP32 ROM specific somehow...
            clk,q,d,hd,cs = values
            value = (hd << 24) | (cs << 18) | (d << 12) | (q << 6) | clk
        else:
            raise argparse.ArgumentError(self, '%s is not a valid spi-connection value. ' +
                                         'Values are SPI, HSPI, or a sequence of 5 pin numbers CLK,Q,D,HD,CS).' % value)
        setattr(namespace, self.dest, value)


class AddrFilenamePairAction(argparse.Action):
    """ Custom parser class for the address/filename pairs passed as arguments """
    def __init__(self, option_strings, dest, nargs='+', **kwargs):
        super(AddrFilenamePairAction, self).__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        # validate pair arguments
        pairs = []
        for i in range(0,len(values),2):
            try:
                address = int(values[i],0)
            except ValueError:
                raise argparse.ArgumentError(self,'Address "%s" must be a number' % values[i])
            try:
                argfile = open(values[i + 1], 'rb')
            except IOError as e:
                raise argparse.ArgumentError(self, e)
            except IndexError:
                raise argparse.ArgumentError(self,'Must be pairs of an address and the binary filename to write there')
            pairs.append((address, argfile))

        # Sort the addresses and check for overlapping
        end = 0
        for address, argfile in sorted(pairs):
            argfile.seek(0,2)  # seek to end
            size = argfile.tell()
            argfile.seek(0)
            sector_start = address & ~(ESPLoader.FLASH_SECTOR_SIZE - 1)
            sector_end = ((address + size + ESPLoader.FLASH_SECTOR_SIZE - 1) & ~(ESPLoader.FLASH_SECTOR_SIZE - 1)) - 1
            if sector_start < end:
                message = 'Detected overlap at address: 0x%x for file: %s' % (address, argfile.name)
                raise argparse.ArgumentError(self, message)
            end = sector_end
        setattr(namespace, self.dest, pairs)


# Binary stub code (see flasher_stub dir for source & details)
ESP8266ROM.STUB_CODE = eval(zlib.decompress(base64.b64decode(b"""
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\
""")))
ESP32ROM.STUB_CODE = eval(zlib.decompress(base64.b64decode(b"""
eNqNWvtz2zYS/ldkJX42vQNIigIzvYvteORXp7WTnur0PHMlQbLpTM91XOXspMn97YdvHyQoye39IBkCwcXuYvfbB/z79qJ5WGw/H1Xb1w+tG4Wv7AVGhkb5wfWDCcPChp91+LTXD96MeNK560X4xsg8nZ/wU1pZ\
/j8rLegZXqAfa5QDE42ij1OOmkl47EFpI3xVTNJ4LIk3LsLfRLiSRQ7jYonDInnLg37Ggdb8w6oogeKnMJtAmrEZ4UG2Xhxj9pnfRpkN6/JAu+xZaepIcX6ZrWJJoCFX6/eUj+3HzvRve5xs/YIJ6IcWZqPozDeU\
m2Qs8uUvw2ACSVwvSVPy03KiCnaHfA5Yhb82uwRZPJqGdZit3Bg8pTjvwJBPL1mdRNQzQefG+2GttZthPo1OzsgYYhGFaHJ47ml4UieDJ6/84JSvsGr+ntneTzFfHLrx2cvT8ZJyHf8lg7Q++qEqph+FifRr3L6M\
XHQExF0W/97f19EJT9M7dkA36+j2p0MqhfBTDA50MBAuOXsJU7ODBzvhKx+NFnKCCXzT50/wKCxuGl5c2X7c6bVMtmRAnwUffNmIeQVyXgyCTLvsTbsR7+teLMQeXex0VbLbA04jdgZvgdsV4SytHEQhH2jBBtK+\
YA15meso+uRK3ghUimogy6n6fk+X2LaRiQm9Ygpu/x6/7iJBTS9oXYupY0NbzBiAjPnEArnwxELN4cli6LFCesXlMZF1dB5Hh6JnqLYdIAJ4S/aVCO1EKaYabwnhBEYQ3lRkxDhTdAj25oe28IZfGSLQxZcwLcG8\
8FUSgavsIvVibCk87gqo8MPri+vrsMbl+nbTH7lzR+HtXM6F4OAp646AJmH8V7XHkIpjsRm0lAKZq2QkuCFA0ETe7PzzMVukz3a/28GLz8e7+LOTkT5MsQzsbhiVyHVvyYlC1Htx8pTkx/oxa6Lso5VqtqwZnF0E\
+D1Xf7u+EdyEkJ6diIKOZUstk94DMG8V7iwrp26ieCJCl7YH0aWgXNJoFM8nP6szboipw8TbVQyOdVmaJwLISzGJDEhDjNHw7eyDsJkwDyzeCZ5COH+gMTmJcwqasbuO2INbluO91Hx1IKE/KU52r4Sgj0MVcVek\
6yLmM+ahC9VQgFAwclgJmx7hhOUTwPO6EnVUa9Sha/yMDXg5PLuYiBDHy0Qw/wOCtazJVtewcCzGc9DLe9BQGvrbVmNJoirFq0TgdG1epuOr+EfAtBoWPgkmX7u/iPEXPppGsISM4Ue+scE8AJ2sgK3migO/zHto\
vOzVUZHjXLwMFH0taYcezyNaa/1ev7gSx1thIV1+8WzMycDcc9pLDiCuWkVvA8jLUmJAs+bQMF9EiU2l72yqbQIxUzkqGyudkMmvOw610zKyU3Dg/RoOSEHwlnQk5z0Rl1h+2z1mUBi/jY/9Nv6xiH88LFmHjYHA\
/ySQibAgPoe93or3bZS9w9K5aJ5Ztqw25xB13KmoCwqdVHoaz65vXum6R6yBxKTjOA4KcWI6eRqpKo9Xrb7Nh/wO6KK8ga2PB6fivZxGyWLi/4KBxxtdLHDueoMszMkjNu3NuqjFQcFHqQrpIjukWPiZyXhZQqqq\
+mOo4m2s2ISAydBTfkQIlvBZTVd95OwfYbKacJ5AWQcJHKyjmKwX2E2DXkvPTGlWSplCnas+j1j7XSbzyDlqhqNbVMmOhtqPStPENCWRANIF7d3BQo6vb8LaysMZzhUW74W7Lvf5xMlrJSmdL2E9xt1tgfKUH5jk\
nlUBNIDXFz7CrJwdgZBC2C8eQYviMbTgMvEZsgMyjOSPvFXzRDjdi29PYJ3wOcrB6xcZ242p9sVwuMygciV7sVQUrqkoYYBuEBz2ByXvclZLXIhR6o+gj+2IQhYVO5pdKAsR55ruCpGqL7c+vZWtG0GZK80s93/Z\
o7jkEglPNnsmI+959DX/gcVNhAywtGBxHjiuGc6BQhy76tDra47jQC9xNmTKdds55c0YcRAlcWmWUSQ+vA2OmFTP1drMGIQEAExyPp4mWlmfM4R7O2oUB7T6aDYkDWy4jKsnEUr4vSc9+JtJl/glVcTginV17vSK\
7dTYQTkZVHpzMe6zyN3egd30EQeu1ijBFyuVasKHUZXsFD7bR22O8OiTuMswYktBCmrEeWibNXlSGzlQbb+VLaPJSrIEKBC6KPUYfOd/7RruqzbS82QvDVMFpmC9dfLFQCzkovndirSpijMotNLDA8h8KOmbpUXb\
NGnvLq8Xby63uElgUF366T1TsM1MudNX07u+3HPmCARuj0YtBsnJuNsUeXh2eik+1Bmh2LFNDi+pdlhKIWy9qmtI4yq1VUixybGpbf+Yp3dStrS3twCGYwZaO423bfpArJPwLYQ0n61Pc6xdwyNqXQLsu4GGqWSj\
yn+quQIjtzH3xTftT33V7KdiWfn9qJ3q/K1OUsBoCfEIhb4XaMw3MaB4ksy4LxR+ft9vVqbK4bhXZ7HEFRgocuaKNrqPCEx6EXE8BqXYQJzonKoB4RkrjBntOyTWL21v8kPe+4tWgyHe+EaXXy+ILS9twYJjGZBn\
qNq8S/67tBEOb1e2m+vDp8fx9C+Yng2THa0u0QYc7pZ0+mqiZYaX2Ok4mrQ6aaJarnuaDnRWRIW6YfQZHtWxZCmkgjteRQlvPoCZsNuckpBtnMJiXb29kKZOztnGMFpviTVlSo1NoKB+xCGMKbnDd4psDdipDbUq\
m7MhtM0m52rBA4844GMbJCSUH7koQuODit3Zt8uczp8jPgdBa8QBlA6l5AEB1SGceokS4o7bnA2ubSKVl/JBBePsSt043+Ni1tlz7d/dq9+fSWLKe9+H9U3GqjPpcHuR42qtHMWqHIFRJIGB0R+x7E7RRg+AjO33\
+NBnr5YOCo0MyGTy1xEJY+URk3ivPZkx81zSIGm4IO3yBRdb0IAAqflAgnGBlGRggz45Zl9jZ/q3bOcQ79GuZ4qb3JXjlsp7NcC30aYIeFX27OAv2o5bv1GpG9XDjR4SxrdGKpMylea2mXI4Bl41doQIZ9/Uh3Cx\
Lz48ZdIoO1z6mZoH+T/7RjJdETQ97pQJ9xeUo5xaiDf4fniDLcaHEkCQChbSWo4jSWE+clnHGYG6eyOOPGi6lHxE+FBG77hjTfPUxDXHe9yq6/ozEw2NclGAtdaici5H+ijv5TEcNMWAs27JVOIpNT3M0agTRuK4\
p9pzwZI4ut9BokcdizqC6UR9cKgwqfwLl+m8m0svkhp7R9QR+A68fhXl+p7XdMwLPBHEZgqTYscNUofWwe1gIB7WVFHrjK6Q7PUaZAyEbzrznCUDhzhS+n/VJv5YarSJRDu7th0VdTCXzdlEXmbyPcqeyIwllfrQ\
ozAdSE43KO2RhNhSOw1DoqD1JMKJoT/PRnpUTr3i1cNYrwowDydtaOvPIlzOZte1ASx34/G2HkFNl3Od7Qd6tXTxKIalCJDvMbjlreyKMvL5bq9LSqkafVRIDe6Ovzrelzwyi+Rtqa3xuWt/t92Nx0c2wcL9fH5P\
G98IZ+1HtDFuuTfnzfGU2bH5KcsG3cLlGkqLZpyIdpUtCd0yTMPwgBS+Zo10vu5OQnYNK6OniDnNPmdVLn3D/XOBQVbErURmbFlLR95pued4ruHwvdk/GSapuaBVH3uOxWnj3LTlLP/FMflNe6Q4f0/mVatB/peC\
TNZninT13YgTN51Pbt9LBUHL3mEelElLpKnuOeU44hatWpCJ4KFOiLNz/ZnRz19nconQ9N0O4B9+U4epXhb7gG8W2walgLwZ1ycXUC9ArcqojJXKgRoS5yMBigrTNOCAyZvCjbz02Kp0eWM5kFRu7CJGV6qGNpYf\
oo+lqNZr8z5gu/Emq7CFaVO532hQ10roMK6EwoNKcL+qRrzMV+yZVE7JvWU5+a3PAKjebf6ktPoVAB/7Od1AmCO6patZJQi0Vnpe4LrQa5n4VqFISs6gm8kPep+zwTOBw23pNOYS8DO6ntvmjAnOicK4mbxac4vH\
L0N0n6noIi61z9acmc3Pur453eh9jxu96Rnd6E13pvsQ2JxO2fSrUsCJ9SRRrlPVPQfUwtwjmvLWd1zntaZ3C5Prjar9QI2XOwmdfI99VzLoN9SuMNQMyne25P0SMlLBRC79vM98oBtvFUWa1/3VprcbtwJRUmoo\
qpT2V+n4SBPXa8XtObugseMWEfeXH1aV6Cl4Vm4L273TdItVWlWMUFWBp5pcV3yNiB5r6eQ+BCsBvCgfOKkeUVEh940l9dFGPUXqtpVcptGFmKq44ZoMMEB3i/ofJ9HNnOrMq84mXnNceUBq26WLcFyqtvWO4yYm\
zJCyuVZa7Zrq1Tkd31yS65zb0KXX7tWX4j9kaNPTqxmzFt74hd0fvzxldAe7WKtG6Xa/m3G/Wn3fIc3vFxS7IIY2JC/YGc8lN1SRKbjO10CWPVQwvVh96uzr5cnZ526ThDnGPmhv9Pt882fQeLK6gMaaduX/4QUW\
TQKqzvKFzESXlRLPk/juVbphhEySUnqoVO/GKSub9rHckMuln7hj1+dsW7zcTLfGgh9LVd/KbazZfaL7Ip3zYyXcJrMI/k2ENjXVspyaMIP0zpeyPF+9A+52rPV/yVTQfEBi3DM27O9vPxvR/+7967dFeYf/4LNm\
mk0SY/IsPGluFncfukmb5SZM1uWilH/1i/ro2/IkJpTmZjLJzOf/AakDVPI=\
""")))
ESP32S2ROM.STUB_CODE = eval(zlib.decompress(base64.b64decode(b"""
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\
""")))


def _main():
    try:
        main()
    except FatalError as e:
        kprint('\nA fatal error occurred: %s' % e)
        sys.exit(2)


if __name__ == '__main__':
    _main()
