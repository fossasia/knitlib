
import logging
import knitting_plugin


class DummyKnittingPlugin(knitting_plugin.BaseKnittingPlugin):

  def __init__(self):
    super(DummyKnittingPlugin, self).__init__()

  base_log_string = "{} has been called on dummy knitting plugin."

  def onknit(self, e):
    logging.debug(DummyKnittingPlugin.base_log_string.format("onknit"))

  def onfinish(self, e):
    logging.debug(DummyKnittingPlugin.base_log_string.format("onfinish"))

  def onconfigure(self, e):
    logging.debug(DummyKnittingPlugin.base_log_string.format("onconfigure"))

  def publish_options(self):
    logging.debug(DummyKnittingPlugin.base_log_string.format("pub options"))
