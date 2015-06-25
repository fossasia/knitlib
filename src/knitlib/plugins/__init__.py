# -*- coding: utf-8 -*-
from enum import Enum

import dummy_plugin
import ayab_plugin
import pdd_plugin


PluginType = Enum('PluginType', 'serial network other')
'''PluginTypes holds an enumeration of the type of machine plugins available for use.'''

active_plugins = {
    PluginType.other: {dummy_plugin.DummyKnittingPlugin.__name__: dummy_plugin.DummyKnittingPlugin},
    PluginType.serial: {ayab_plugin.AyabPluginControl.__name__: ayab_plugin.AyabPluginControl,
                        pdd_plugin.PDDEmulationKnittingPlugin.__name__: pdd_plugin.PDDEmulationKnittingPlugin,
                        }
}
