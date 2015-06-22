# -*- coding: utf-8 -*-
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

  def open_serial(self, pPortname=None, baudrate=None):
    """Opens serial port communication with a portName and baudrate."""
    if not self.__ser:
      self.__portname = pPortname
      self.__baudrate = baudrate
      try:
          self.__ser = serial.Serial(self.__portname, self.__baudrate)
          time.sleep(1)
      except:
        self.__logger.error("could not open serial port " + self.__portname + "with specific baudrate " + self.__baudrate)
        raise CommunicationException()
      return True

  def close_serial(self):
    """Closes serial port."""
    try:
      self.__ser.close()
      del(self.__ser)
      self.__ser = None
    except:
      raise CommunicationException()


class CommunicationException(Exception):
  pass
