# -*- coding: utf-8 -*-
# This file is part of AYAB.
#
#    AYAB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AYAB is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AYAB.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2013 Christian Obersteiner, Andreas Müller
#    https://bitbucket.org/chris007de/ayab-apparat/

"""Handles the serial communication protocol.

This module handles serial communication, currently works in a synchronous way.
AyabCommunication uses an internal PySerial.Serial object to connect to the device.
The initializer can also be overriden with a dummy serial object.
"""

import time
import serial

import logging

from knitlib.exceptions import CommunicationException


class AyabCommunication(object):
  """Class Handling the serial communication protocol."""

  def __init__(self, serial=None):
    """Creates an AyabCommunication object, with an optional serial-like object."""
    logging.basicConfig(level=logging.DEBUG)
    self.__logger = logging.getLogger(__name__)
    self.__ser = serial

  def __del__(self):
    """Handles on delete behaviour closing serial port object."""
    self.close_serial()

  def open_serial(self, serial_port_name=None, serial_port_speed=115200):
    """Opens serial port communication with a portName."""
    if not self.__ser:
      self.__portname = serial_port_name
      try:
          self.__ser = serial.Serial(self.__portname, serial_port_speed)
          time.sleep(1)
      except:
        self.__logger.error("could not open serial port " + self.__portname)
        raise CommunicationException()
      return True
    else:
      self.__logger.error("could not open serial port ")
      raise CommunicationException()

  def close_serial(self):
    """Closes serial port."""
    try:
      self.__ser.close()
      del(self.__ser)
      self.__ser = None
    except:
      # TODO: add message for closing serial failure.
      raise CommunicationException()

  def read_line(self):
    """Reads a line from serial communication."""
    line = bytes()
    if self.__ser:
      while self.__ser.inWaiting() > 0:
          line += self.__ser.read(1)
    return line

  def write_line(self, line):
    """Writes a line """
    if self.__ser:
      while line.length > 0:
          self.__ser.write(line)
    return line

  def write_byte(self, byte):
    """Writes a byte"""
    if self.__ser:
      while byte.length > 0:
          self.__ser.write(byte)
    return byte

  def req_start(self, startNeedle, stopNeedle):
      """Sends a start message to the controller."""

      msg = chr(0x01)  # msg id
      msg += chr(int(startNeedle))
      msg += chr(int(stopNeedle))
      # print "< reqStart"
      self.__ser.write(msg + '\n\r')

  def req_info(self):
      """Sends a request for information to controller."""
      # print "< reqInfo"
      self.__ser.write(chr(0x03) + '\n\r')

  def cnf_line(self, lineNumber, lineData, flags, crc8):
      """Sends a line of data via the serial port.

      Sends a line of data to the serial port, all arguments are mandatory.
      The data sent here is parsed by the Arduino controller which sets the
      knitting needles accordingly.

      Args:
        lineNumber (int): The line number to be sent.
        lineData (bytes): The bytearray to be sent to needles.
        flags (bytes): The flags sent to the controller.
        crc8 (bytes, optional): The CRC-8 checksum for transmission.

      """

      msg = chr(0x42)                    # msg id
      msg += chr(lineNumber)              # line number
      msg += lineData                     # line data
      msg += chr(flags)                   # flags
      msg += chr(crc8)                    # crc8
      # print "< cnfLine"
      # print lineData
      self.__ser.write(msg + '\n\r')
