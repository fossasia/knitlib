import dummy_plugin
import ayab_plugin

from enum import Enum

PluginType = Enum('PluginType', 'serial network other')
'''PluginTypes holds an enumeration of the type of machine plugins available for use.'''

active_plugins = {
    PluginType.other: {dummy_plugin.DummyKnittingPlugin.__name__: dummy_plugin.DummyKnittingPlugin,
                       ayab_plugin.AyabPluginControl.__name__: ayab_plugin.AyabPluginControl
                       },
}
