# This file is based on Ayab

"""Handles the serial communication protocol.
"""

import time
import serial

import logging


class Communication(object):
  """Class Handling the serial communication protocol."""

  def __init__(self, serial=None):
    """Creates an Communication object, with an optional serial-like object."""
    logging.basicConfig(level=logging.DEBUG)
    self.__logger = logging.getLogger(__name__)
    self.__ser = serial

  def __del__(self):
    """Handles on delete behavior closing serial port object."""
    self.close_serial()

  def open_serial(self, pPortname=None):
    """Opens serial port communication with a portName."""
    if not self.__ser:
      self.__portname = pPortname
      try:
          self.__ser = serial.Serial(self.__portname, 115200)
          time.sleep(1)
      except:
        self.__logger.error("could not open serial port " + self.__portname)
        raise CommunicationException()
      return True

  def close_serial(self):
    """Closes serial port."""
    try:
      self.__ser.close()
      del(self.__ser)
      self.__ser = None
    except:
      #TODO: add message for closing serial failure.
      raise CommunicationException()

  def read_line(self):
    """Reads a line from serial communication."""
    line = bytes()
    if self.__ser:
      while self.__ser.inWaiting() > 0:
          line += self.__ser.read(1)
    return line


class CommunicationException(Exception):
  pass


