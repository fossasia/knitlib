# -*- coding: utf-8 -*-
import plugins
import serial.tools.list_ports

"""Handles allocation of machines to plugins and resources.

Machine Plugins are defined as subclasses of BaseKnittingPlugin. Each Machine
plugin can be matched to a port or interface. Each port can only handle one
machine at once.
"""


def get_available_ports():
  """Returns a list tuples of available serial ports."""
  # TODO: add other kinds of ports listing.
  return list(serial.tools.list_ports.comports())


def get_machines_by_type(machine_type):
  """Returns a list of the available plugins for a given PluginType or empty array if none found."""
  return plugins.active_plugins.get(machine_type, {})


def get_machine_plugin_by_id(machine_id):
  """Returns a machine plugin given the machine_id class name."""
  for k, v in plugins.active_plugins.items():
    if machine_id in v:
      return v[machine_id]


def get_machine_types():
  """Returns the PluginType Enum."""
  return plugins.PluginType
