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
#    Copyright 2015 Shiluka Dharmasena, Sebastian Oliva, Christian Obersteiner, Andreas Müller
#    https://bitbucket.org/chris007de/ayab-apparat/

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
