__author__ = 'tian'

import os
import shutil
# import fs
import sys
import logging
import tempfile
import PDDemulate
from PDDemulate import PDDemulator
from knitlib.plugins.knitting_plugin import BaseKnittingPlugin
import knitlib.exceptions


class PDDEmulationKnittingPlugin(BaseKnittingPlugin):

    __PLUGIN_NAME__ = u"PDD"

    def __init__(self, callbacks_dict=None, interactive_callbacks=None):
        super(PDDEmulationKnittingPlugin, self).__init__(callbacks_dict, interactive_callbacks)
        logging.debug("Loaded PDD emulator version: {}".format(PDDemulate.version))
        self.__port = ""
        self.__conf = None
        self.__main_temp_dir = tempfile.gettempdir()
        self.__folder = os.path.join(self.__main_temp_dir, "PDD_tmp_dir")
        self.__emu = None
        # TODO: init emulator

    def register_interactive_callbacks(self, callbacks=None):
        super(PDDEmulationKnittingPlugin, self).register_interactive_callbacks(callbacks)

    def set_port(self, portname):
        self.__port = portname

    def onconfigure(self, e):
        if hasattr(e, "conf") and e.conf is not None:
            self.__conf = e.conf
        else:
            raise knitlib.exceptions.InputException("Conf dict is missing")

        conf = self.__conf
        if self.__port is "":
            self.__port = conf.get("port", "/dev/ttyUSB0")

        try:
            os.mkdir(self.__folder)
        except OSError:
            # Exception thrown meaning the folder already exists
            logging.warning("PDD temp folder already exists")

        # Copying the image file to temp folder.
        try:
            shutil.copy(conf.get("file_url"), self.__folder)
        except IOError:
            logging.error("Error when copying file url")

        self.__emu = PDDemulator(self.__folder)

    def onknit(self, e):
        emu.open(self.__port)
        logging.info("PDD Emulator Ready")
        emu.handleRequests()

    def validate_configuration(self, conf):
        # TODO validate formally
        return True

    def onfinish(self, e):
        # TODO: remove and cleanup dir at self.__folder
        emu.close()

    @staticmethod
    def supported_config_features():
        return {"$schema": "http://json-schema.org/schema#", "type": "object"}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Usage: %s basedir serialdevice' % sys.argv[0]
        sys.exit()

    print 'Preparing . . . Please Wait'
    emu = PDDemulator(sys.argv[1])

    # TODO: fix usb port hardcoding
    emu.open(cport=sys.argv[2])

    print 'Emulator Ready!'
    try:
        while 1:
            emu.handleRequests()
    except (KeyboardInterrupt):
        pass

    emu.close()
