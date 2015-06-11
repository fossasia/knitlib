
import logging
import knitting_plugin


class DummyKnittingPlugin(knitting_plugin.BaseKnittingPlugin):

  def __init__(self):
    super(DummyKnittingPlugin, self).__init__()
    self.register_interactive_callbacks()

  base_log_string = "{} has been called on dummy knitting plugin."

  def onknit(self, e):
    logging.debug(DummyKnittingPlugin.base_log_string.format("onknit"))

  def onfinish(self, e):
    logging.debug(DummyKnittingPlugin.base_log_string.format("onfinish"))

  def onconfigure(self, e):
    logging.debug(DummyKnittingPlugin.base_log_string.format("onconfigure"))

  def publish_options(self):
    logging.debug(DummyKnittingPlugin.base_log_string.format("pub options"))

  def __interactive_info(message):
    logging.info(message)
    raw_input()

  def __interactive_warn(message):
    logging.info(message)
    raw_input()

  def __interactive_error(message):
    logging.error(message)
    raw_input()

  def __log_progress(message):
    logging.info(message)

  def register_interactive_callbacks(self):
    callbacks = {
        "info": DummyKnittingPlugin.__interactive_info,
        "warning": DummyKnittingPlugin.__interactive_warn,
        "error": DummyKnittingPlugin.__interactive_error,
        "progress": DummyKnittingPlugin.__log_progress
    }
    super(DummyKnittingPlugin, self).register_interactive_callbacks(callbacks)





