__author__ = 'tian'

import sys
import logging
import PDDemulate
from PDDemulate import PDDemulator
from knitlib.plugins.knitting_plugin import BaseKnittingPlugin


class PDDEmulationKnittingPlugin(BaseKnittingPlugin):

    __PLUGIN_NAME__ = u"PDD"

    def __init__(self, callbacks_dict=None, interactive_callbacks=None):
        super(PDDEmulationKnittingPlugin, self).__init__(callbacks_dict, interactive_callbacks)
        logging.debug("Loaded PDD emulator version: {}".format(PDDemulate.version))
        # TODO: init emulator

    def register_interactive_callbacks(self, callbacks=None):
        super(PDDEmulationKnittingPlugin, self).register_interactive_callbacks(callbacks)

    def validate_configuration(self, conf):
        pass

    def publish_options(self):
        pass

    def onfinish(self, e):
        pass

    def onconfigure(self, e):
        pass

    def onknit(self, e):
        pass

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
