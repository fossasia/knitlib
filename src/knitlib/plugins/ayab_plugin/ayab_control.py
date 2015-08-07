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
#    Copyright 2013, 2014 Sebastian Oliva, Christian Obersteiner, Andreas Müller
#    https://bitbucket.org/chris007de/ayab-apparat/

from ayab_communication import AyabCommunication
import ayab_image
import time
import logging
import os
from PIL import Image
from knitlib.plugins.knitting_plugin import BaseKnittingPlugin
from knitlib import knitpat


class AyabPluginControl(BaseKnittingPlugin):

    __PLUGIN_NAME__ = "AYAB"

    def __init__(self):
        super(AyabPluginControl, self).__init__()
        # KnittingPlugin.__init__(self)

        # From AYAB's ayab_control
        self.__API_VERSION = 0x03
        self.__ayabCom = AyabCommunication()

        self.__formerRequest = 0
        self.__lineBlock = 0

    def __del__(self):
        self.__close_serial()

    def onknit(self, e):
        logging.debug("called onknit on AyabPluginControl")
        self.__knitImage(self.__image, self.conf)
        self.finish()

    def onconfigure(self, e):
        logging.debug("called onconfigure on AYAB Knitting Plugin")
        logging.debug("With args: {}".format(e.args))
        logging.debug("With conf kwarg: {}".format(e.conf))

        # Start to knit with the bottom first
        # pil_image = self.pil_image.rotate(180)

        # conf = e.event.conf
        # self.conf = e.event.conf
        if hasattr(e, "conf") and e.conf is not None:
            if knitpat.validate_dict(e.conf):
                conf = e.conf
            else:
                conf = self.generate_test_configuration()

        else:
            conf = self.generate_test_configuration()

        self.conf = conf
        logging.debug("Working with final conf: {}".format(e.conf))

        script_dir = os.path.dirname(os.path.abspath(__file__))  # Temp fix for testing Image opening
        pil_image = Image.open(os.path.join(script_dir, conf["file_url"]))

        try:
            self.__image = ayab_image.ayabImage(pil_image, self.conf["num_colors"])
        except:
            self.__notify_user("You need to set an image.", "error")
            return

        if conf.get("start_needle") and conf.get("stop_needle"):
            self.__image.setKnitNeedles(conf.get("start_needle"), conf.get("stop_needle"))
            if conf.get("alignment"):
                self.__image.setImagePosition(conf.get("alignment"))
        if conf.get("start_line"):
            self.__image.setStartLine(conf.get("start_line"))

            # Do Knit.

    def onfinish(self, e):
        logging.info("Finished Knitting.")
        self.__close_serial()
        # self.__parent_ui.resetUI()
        # self.__parent_ui.emit(QtCore.SIGNAL('updateProgress(int,int,int)'), 0, 0, 0)

    @property
    def supported_config_features(self):
        return {
            "$schema": "http://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "start_needle": {"type": "integer"},
                "stop_needle": {"type": "integer"},
                "start_line": {"type": "integer"},
                "machine_type": {"type": "string",
                                 "enum": ["single", "double"]},
                "alignment": {"type": "string",
                              "enum": ["left", "center", "right"]},
                "inf_repeat": {"type": "integer"}
            }
        }

    def cancel(self):
        self._knitImage = False
        # self.finish()

    def __close_serial(self):
        try:
            self.__ayabCom.close_serial()
            logging.debug("Closing Serial port successful.")
        except:
            logging.debug("Closing Serial port failed. Was it ever open?")

    def onerror(self, e):
        # TODO add message info from event
        logging.error("Error while Knitting.")
        self.__close_serial()

    def validate_configuration(self, conf):
        if conf.get("start_needle") and conf.get("stop_needle"):
            if conf.get("start_needle") > conf.get("stop_needle"):
                self.__notify_user("Invalid needle start and end.", "warning")
                return False
        if conf.get("start_line") > self.__image.imgHeight():
            self.__notify_user("Start Line is larger than the image.")
            return False

        if conf.get("portname") == '':
            self.__notify_user("Please choose a valid port.")
            return False
        return True

    def __wait_for_user_action(self, message="", message_type="info"):
        """Waits for the user to react, blocking it."""
        self.interactive_callbacks["blocking_user_action"](message, message_type)
        # TODO: should be replaced by self.interactive_callbacks["user_action"]
        # logging.info(message)
        # time.sleep(3)
        # raw_input()
        # pass
        # self.__parent_ui.emit(QtCore.SIGNAL('display_blocking_pop_up_signal(QString, QString)'), message, message_type)

    def __notify_user(self, message="", message_type="info"):
        """Sends the a notification without blocking."""
        self.interactive_callbacks["message"](message, message_type)
        # TODO: should be replaced by self.interactive_callbacks["info"]
        # logging.info(message)
        # pass
        # self.__parent_ui.emit(QtCore.SIGNAL('display_pop_up_signal(QString, QString)'), message, message_type)

    def __emit_progress(self, percent, done, total):
        """Shows the current job progress."""
        self.interactive_callbacks["progress"](percent, done, total)
        # TODO: should be replaced by self.interactive_callbacks["progress"]
        # logging.info("Knitting at {}% . {} out of {}.".format(percent, done, total))
        # pass
        # self.__parent_ui.emit(QtCore.SIGNAL('updateProgress(int,int,int)'), int(percent), int(done), int(total))

    def generate_test_configuration(self):
        """Creates a configuration dict from the ui elements.

        Returns:
          dict: A dict with configuration.

        """

        conf = {}
        conf[u"num_colors"] = 2
        conf[u"start_line"] = 0

        start_needle_color = stop_needle_color = u"orange"  # or green.
        start_needle_value = stop_needle_value = 0

        def set_value_by_color(conf_dict, needle_position, needle_color, start_needle_value):
            if needle_color == u"orange":
                conf_dict[needle_position] = 100 - start_needle_value
            elif needle_color == u"green":
                conf_dict[needle_position] = 99 + start_needle_value
            else:
                conf_dict[needle_position] = start_needle_value
            return conf_dict

        conf = set_value_by_color(conf, u"start_needle", start_needle_color, start_needle_value)
        conf = set_value_by_color(conf, u"stop_needle", stop_needle_color, stop_needle_value)

        conf["alignment"] = "center"
        conf["inf_repeat"] = 0
        conf["machine_type"] = "single"

        # serial_port = u"/dev/ttyACM0"
        # conf["portname"] = serial_port  # Should be related to self.getSerialPorts()[0][0]
        self.set_port()
        # getting file location from textbox
        filename_text = u"mushroom.png"
        conf["file_url"] = filename_text
        logging.debug(conf)
        # TODO: Add more config options.
        return conf

    def set_port(self, port_name=u"/dev/ttyACM0"):
        self.conf["portname"] = port_name

    # From ayab_control
    #####################################

    def __setBit(self, int_type, offset):
        mask = 1 << offset
        return (int_type | mask)

    def __setPixel(self, bytearray, pixel):
        numByte = int(pixel / 8)
        bytearray[numByte] = self.__setBit(
            int(bytearray[numByte]), pixel - (8 * numByte))
        return bytearray

    def __checkSerial(self):
        time.sleep(1)  # TODO if problems in communication, tweak here

        line = self.__ayabCom.read_line()

        if line != '':
            msgId = ord(line[0])
            if msgId == 0xC1:  # cnfStart
                # print "> cnfStart: " + str(ord(line[1]))
                return ("cnfStart", ord(line[1]))

            elif msgId == 0xC3:  # cnfInfo
                # print "> cnfInfo: Version=" + str(ord(line[1]))
                logging.debug("Detected device with API v" + str(ord(line[1])))
                return ("cnfInfo", ord(line[1]))

            elif msgId == 0x82:  # reqLine
                # print "> reqLine: " + str(ord(line[1]))
                return ("reqLine", ord(line[1]))

            else:
                self.__printError("unknown message: " + line[:])  # drop crlf
                return ("unknown", 0)
        return ("none", 0)

    def __cnfLine(self, lineNumber):
        imgHeight = self.__image.imgHeight()
        color = 0
        indexToSend = 0
        sendBlankLine = False
        lastLine = 0x00

        # TODO optimize performance
        # initialize bytearray to 0x00
        bytes = bytearray(25)
        for x in range(0, 25):
            bytes[x] = 0x00

        if lineNumber < 256:
            # TODO some better algorithm for block wrapping
            # if the last requested line number was 255, wrap to next block of
            # lines
            if self.__formerRequest == 255 and lineNumber == 0:
                self.__lineBlock += 1
            # store requested line number for next request
            self.__formerRequest = lineNumber
            reqestedLine = lineNumber

            # adjust lineNumber with current block
            lineNumber = lineNumber + (self.__lineBlock * 256)

            # when knitting infinitely, keep the requested lineNumber in its limits
            if self.__infRepeat:
                lineNumber = lineNumber % imgHeight

            #########################
            # decide which line to send according to machine type and amount of colors
            # singlebed, 2 color
            if self.__machineType == 'single' and self.__numColors == 2:

                # color is always 0 in singlebed,
                # because both colors are knitted at once
                color = 0

                # calculate imgRow
                imgRow = lineNumber + self.__startLine

                # 0   1   2   3   4 .. (imgRow)
                # |   |   |   |   |
                # 0 1 2 3 4 5 6 7 8 .. (imageExpanded)
                indexToSend = imgRow * 2

                # Check if the last line of the image was requested
                if imgRow == imgHeight - 1:
                    lastLine = 0x01

            # doublebed, 2 color
            elif self.__machineType == 'double' \
                    and self.__numColors == 2:

                # calculate imgRow
                imgRow = int(lineNumber / 2) + self.__startLine

                # 0 0 1 1 2 2 3 3 4 4 .. (imgRow)
                # 0 1 2 3 4 5 6 7 8 9 .. (lineNumber)
                # | |  X  | |  X  | |
                # 0 1 3 2 4 5 7 6 8 9 .. (imageExpanded)
                lenImgExpanded = len(self.__image.imageExpanded())
                indexToSend = self.__startLine * 2

                # TODO more beautiful algo
                if lineNumber % 4 == 1 or lineNumber % 4 == 2:
                    color = 1
                else:
                    color = 0

                if (lineNumber - 2) % 4 == 0:
                    indexToSend += lineNumber + 1

                elif (lineNumber - 2) % 4 == 1:
                    indexToSend += lineNumber - 1
                    if (imgRow == imgHeight - 1) \
                            and (indexToSend == lenImgExpanded - 2):
                        lastLine = 0x01
                else:
                    indexToSend += lineNumber
                    if (imgRow == imgHeight - 1) \
                            and (indexToSend == lenImgExpanded - 1):
                        lastLine = 0x01

            # doublebed, multicolor
            elif self.__machineType == 'double' \
                    and self.__numColors > 2:

                # calculate imgRow
                imgRow = int(
                    lineNumber / (self.__numColors * 2)) + self.__startLine

                if (lineNumber % 2) == 0:
                    color = (lineNumber / 2) % self.__numColors
                    indexToSend = (imgRow * self.__numColors) + color
                    logging.debug("COLOR" + str(color))
                else:
                    sendBlankLine = True

                lenImgExpanded = len(self.__image.imageExpanded())

                # TODO Check assignment
                if imgRow == imgHeight - 1 \
                        and (indexToSend == lenImgExpanded - 1):
                    lastLine = 0x01
            #########################

            # assign pixeldata
            imgStartNeedle = self.__image.imgStartNeedle()
            if imgStartNeedle < 0:
                imgStartNeedle = 0

            imgStopNeedle = self.__image.imgStopNeedle()
            if imgStopNeedle > 199:
                imgStopNeedle = 199

            # set the bitarray
            if color == 0 \
                    and self.__machineType == 'double':
                for col in range(0, 200):
                    if col < imgStartNeedle \
                            or col > imgStopNeedle:
                        bytes = self.__setPixel(bytes, col)

            for col in range(0, self.__image.imgWidth()):
                pxl = (self.__image.imageExpanded())[indexToSend][col]
                # take the image offset into account
                if pxl is True and sendBlankLine is False:
                    bytes = self.__setPixel(
                        bytes, col + self.__image.imgStartNeedle())

            # TODO implement CRC8
            crc8 = 0x00

            # send line to machine
            if self.__infRepeat:
                self.__ayabCom.cnf_line(reqestedLine, bytes, 0, crc8)
            else:
                self.__ayabCom.cnf_line(reqestedLine, bytes, lastLine, crc8)

            # screen output
            msg = str((self.__image.imageExpanded())[indexToSend])
            msg += ' Image Row: ' + str(imgRow)
            msg += ' (indexToSend: ' + str(indexToSend)
            msg += ', reqLine: ' + str(reqestedLine)
            msg += ', lineNumber: ' + str(lineNumber)
            msg += ', lineBlock:' + str(self.__lineBlock) + ')'
            logging.debug(msg)
            # sending line progress to gui
            progress_int = 100 * float(imgRow) / self.__image.imgHeight()
            self.__emit_progress(progress_int, imgRow, imgHeight)

        else:
            logging.error("requested lineNumber out of range")

        if lastLine:
            if self.__infRepeat:
                self.__lineBlock = 0
                return 0  # keep knitting
            else:
                return 1  # image finished
        else:
            return 0  # keep knitting

    def __knitImage(self, pImage, pOptions):
        self.__formerRequest = 0
        self.__image = pImage
        self.__startLine = pImage.startLine()

        self.__numColors = pOptions["num_colors"]
        self.__machineType = pOptions["machine_type"]
        self.__infRepeat = pOptions["inf_repeat"]

        API_VERSION = self.__API_VERSION
        curState = 's_init'
        oldState = 'none'

        if not self.__ayabCom.open_serial(pOptions["portname"]):
            logging.error("Could not open serial port")
            return

        self._knitImage = True
        logging.debug("Ready to start knitting process.")
        while self._knitImage:
            # TODO catch keyboard interrupts to abort knitting
            # TODO: port to state machine or similar.
            rcvMsg, rcvParam = self.__checkSerial()
            if curState == 's_init':
                if oldState != curState:
                    self.__ayabCom.req_info()

                if rcvMsg == 'cnfInfo':
                    if rcvParam == API_VERSION:
                        curState = 's_start'
                        self.__wait_for_user_action(
                            "Please init machine. (Set the carriage to mode KC-I or KC-II and move the carriage over the left turn mark).")
                    else:
                        self.__notify_user("Wrong API.")
                        logging.error("wrong API version: " + str(rcvParam)
                                      + (" (expected: )") + str(API_VERSION))
                        return

            if curState == 's_start':
                if oldState != curState:
                    self.__ayabCom.req_start(self.__image.knitStartNeedle(),
                                             self.__image.knitStopNeedle())

                if rcvMsg == 'cnfStart':
                    if rcvParam == 1:
                        curState = 's_operate'
                        self.__wait_for_user_action("Ready to Operate")
                    else:
                        self.__wait_for_user_action("Device not ready, configure and try again.")
                        logging.error("device not ready")
                        return

            if curState == 's_operate':
                if rcvMsg == 'reqLine':
                    imageFinished = self.__cnfLine(rcvParam)
                    if imageFinished:
                        curState = 's_finished'

            if curState == 's_finished':
                self.__wait_for_user_action(
                    "Image transmission finished. Please knit until you hear the double beep sound.")
                return

            oldState = curState

        return
