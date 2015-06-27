# -*- coding: utf-8 -*-
from enum import Enum

import dummy_plugin
import ayab_plugin
import pdd_plugin


PluginType = Enum('PluginType', 'serial network other')
'''PluginTypes holds an enumeration of the type of machine plugins available for use.'''

active_plugins = {
    PluginType.other: {u"dummy": dummy_plugin.DummyKnittingPlugin},
    PluginType.serial: {u"AYAB": ayab_plugin.AyabPluginControl,
                        u"PDD": pdd_plugin.PDDEmulationKnittingPlugin,
                        }
}
