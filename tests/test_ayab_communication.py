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
#    Copyright 2015 Shiluka Dharmasena, Sebastian Oliva, Christian Obersteiner, Andreas M�ller
#    https://bitbucket.org/chris007de/ayab-apparat/

import pytest
import serial
import unittest
from knitlib.plugins.ayab_plugin.ayab_communication import AyabCommunication
from mock import patch


class TestCommunication(unittest.TestCase):

  def setUp(self):
    self.dummy_serial = serial.serial_for_url("loop://logging=debug")
    self.comm_dummy = AyabCommunication(self.dummy_serial)

  """Test on closing serial port communication."""
  def test_close_serial(self):
      before = self.dummy_serial.isOpen()
      assert before
      self.comm_dummy.close_serial()
      after = self.dummy_serial.isOpen()
      assert after == False

  """Test on opening serial port communication with a baudrate 115200."""
  def test_open_serial(self):
    with patch.object(serial,'Serial') as mock_method:
      mock_method.return_value = object()
      self.ayabCom = AyabCommunication()
      openStatus = self.ayabCom.open_serial('dummyPortname')
      assert openStatus
      mock_method.assert_called_once_with('dummyPortname',115200)

    with patch.object(serial,'Serial') as mock_method:
      with pytest.raises(Exception) as excinfo:
        mock_method.side_effect = serial.SerialException()
        self.ayabCom = AyabCommunication()
        openStatus = self.ayabCom.open_serial('dummyPortname')
      assert "CommunicationException" in str(excinfo.type)
      mock_method.assert_called_once_with('dummyPortname',115200)

  """Test on sending a start message to the controller."""
  def test_req_start(self):
    start_val, end_val = 0, 10
    self.comm_dummy.req_start(start_val, end_val)
    byte_array = bytearray([0x01, start_val, end_val, 0x0a, 0x0d])
    bytes_read = self.dummy_serial.read(len(byte_array))
    self.assertEqual(bytes_read, byte_array)

  """Test on Sending a request for information to controller."""
  def test_req_info(self):
    self.comm_dummy.req_info()
    byte_array = bytearray([0x03, 0x0a, 0x0d])
    bytes_read = self.dummy_serial.read(len(byte_array))
    assert bytes_read == byte_array

  """Test on sending a line of data via the serial port."""
  def test_cnf_line(self):
    lineNumber = 13
    lineData   = chr(0xAB)
    flags      = 0x12
    crc8       = 0x57
    self.comm_dummy.cnf_line(lineNumber, lineData, flags, crc8)
    byte_array = bytearray([0x42, lineNumber, lineData, flags, crc8, 0x0a, 0x0d])
    bytes_read = self.dummy_serial.read(len(byte_array))
    assert bytes_read == byte_array

  """Test on reading a line from serial communication."""
  def test_read_line(self):
    byte_start_val = 0x01
    byte_end_val = 0x12
    byte_array = bytearray([0xC1, byte_start_val, byte_end_val, 0x0a, 0x0d])
    bytes_wrote = self.dummy_serial.write(byte_array)
    bytes_read = self.comm_dummy.read_line()
    assert bytes_read == byte_array
