# -*- coding: utf-8 -*-
# This file is part of Knitlib.
#
#    Knitlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Knitlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Knitlib.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2015 Sebastian Oliva, Shiluka Dharmasena <http://github.com/fashiontec/knitlib>


class KnittingError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class InputException(KnittingError):
    """Exception raised for errors in the input.
    Attributes:
        expression -- input expression in which
                          the error occurred
        message -- explanation of the error
    """
    pass


class CommunicationException(KnittingError):
    """Exception raised for errors in the communication.
    Attributes:
        expression -- communication expression in which
                          the error occurred
        message -- explanation of the error
    """
    pass


class PatternNotFoundException(KnittingError):
    """Exception raised for errors in the pattern.
    Attributes:
        expression -- pattern expression in which
                          the error occurred
        message -- explanation of the error
    """
    pass


class InsertPatternException(KnittingError):
    """Exception raised for errors in the insert of the pattern.
    Attributes:
        expression -- insert pattern expression in which
                          the error occurred
        message -- explanation of the error
    """
    pass


class SendDataException(KnittingError):
    """Exception raised for errors in sending data to the serial port.
    Attributes:
        expression -- send data expression in which
                          the error occurred
        message -- explanation of the error
    """
    pass


class OpenSerialException(KnittingError):
    """Exception raised for errors in opening the serial port.
    Attributes:
        expression -- open serial port expression in which
                          the error occurred
        message -- explanation of the error
    """
    pass


class CloseSerialException(KnittingError):
    """Exception raised for errors in closing the serial port.
    Attributes:
        expression -- close serial port expression in which
                          the error occurred
        message -- explanation of the error
    """
    pass


class ReadLineException(KnittingError):
    """Exception raised for errors in reading lines.
    Attributes:
        expression -- send data expression in which
                          the error occurred
        message -- explanation of the error
    """
    pass


class WriteLineException(KnittingError):
    """Exception raised for errors in writing lines.
    Attributes:
        expression -- write lines expression in which
                          the error occurred
        message -- explanation of the error
    """
    pass


class ReadByteException(KnittingError):
    """Exception raised for errors in reading bytes.
    Attributes:
        expression -- read data as bytes expression in which
                          the error occurred
        message -- explanation of the error
    """
    pass


class WriteByteException(KnittingError):
    """Exception raised for errors in writing bytes.
    Attributes:
        expression -- write data as byte expression in which
                          the error occurred
        message -- explanation of the error
    """
    pass
