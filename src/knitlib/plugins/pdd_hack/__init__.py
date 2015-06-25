__author__ = 'tian'

import logging
import PDDemulate
from knitlib.plugins.knitting_plugin import BaseKnittingPlugin


class PDDEmulationKnittingPlugin(BaseKnittingPlugin):
    def __init__(self, callbacks_dict=None, interactive_callbacks=None):
        super(PDDEmulationKnittingPlugin, self).__init__(callbacks_dict, interactive_callbacks)
        logging.debug("Loaded PDD emulator version: {}".format(PDDemulate.version))
        # TODO: init emulator

    def validate_configuration(self, conf):
        pass

    def onfinish(self, e):
        pass

    def onconfigure(self, e):
        pass

    def onknit(self, e):
        pass
