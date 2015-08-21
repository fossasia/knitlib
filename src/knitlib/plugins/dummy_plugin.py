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
#    Copyright 2015 Sebastian Oliva <http://github.com/fashiontec/knitlib>

import logging
import time
import knitting_plugin


class DummyKnittingPlugin(knitting_plugin.BaseKnittingPlugin):
  """Implements a sample knitting plugin that allows for simple operation emulation."""

  __PLUGIN_NAME__ = u"dummy"

  def __init__(self):
    super(DummyKnittingPlugin, self).__init__()

  base_log_string = u"{} has been called on dummy knitting plugin."

  def onknit(self, e):
    logging.debug(DummyKnittingPlugin.base_log_string.format("onknit"))
    # In order to simulate blocking we make it sleep.
    total = 5
    for i in range(total):
      time.sleep(1)
      self.interactive_callbacks["progress"](i / float(total), i, total)
    self.finish()

  def onfinish(self, e):
    logging.debug(DummyKnittingPlugin.base_log_string.format("onfinish"))

  def onconfigure(self, e):
    logging.debug(DummyKnittingPlugin.base_log_string.format("onconfigure"))

  def set_port(self, *args, **kwargs):
    pass

  @staticmethod
  def supported_config_features():
    return {"$schema": "http://json-schema.org/schema#", "type": "object"}
