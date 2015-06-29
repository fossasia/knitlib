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

from enum import Enum

from dummy_plugin import DummyKnittingPlugin
from ayab_plugin import AyabPluginControl
from pdd_plugin import PDDEmulationKnittingPlugin


PluginType = Enum('PluginType', 'serial network other')
'''PluginTypes holds an enumeration of the type of machine plugins available for use.'''

active_plugins = {
    PluginType.other: {DummyKnittingPlugin.__PLUGIN_NAME__: DummyKnittingPlugin},
    PluginType.serial: {AyabPluginControl.__PLUGIN_NAME__: ayab_plugin.AyabPluginControl,
                        PDDEmulationKnittingPlugin.__PLUGIN_NAME__: pdd_plugin.PDDEmulationKnittingPlugin,
                        }
}
