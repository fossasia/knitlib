"""Handles the serial communication protocol.

This module handles serial communication, currently works in a synchronous way.
AyabCommunication uses an internal PySerial.Serial object to connect to the device.
The initializer can also be overriden with a dummy serial object.
"""

import time
import serial

import logging
import serial


class Communication(object):
  """Class Handling the serial communication protocol."""

  def __init__(self, serial=None):
    """Creates an AyabCommunication object, with an optional serial-like object."""
    logging.basicConfig(level=logging.DEBUG)
    self.__logger = logging.getLogger(__name__)
    self.__ser = serial

  def __del__(self):
    """Handles on delete behaviour closing serial port object."""
    self.close_serial()

  def open_serial(self, pPortname=None):
    """Opens serial port communication with a portName."""
    if not self.__ser:
      self.__portname = pPortname
      try:
          self.__ser = serial.Serial(self.__portname, 115200)
          time.sleep(1)
          self__logger.info("opened serial port communication with a portName " + self.__portname)
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


class CommunicationException(Exception):
  pass
