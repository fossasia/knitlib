# -*- coding: utf-8 -*-
import pytest

import knitlib
from knitlib import machine_handler
from knitlib.plugins import knitting_plugin
from knitlib.plugins import dummy_plugin


def test_methods_exception():
  """Tests that abstract methods from BaseKnittingPlugin throw exceptions.

  All methods from BaseKnittingPlugin should fail. Methods from this class
  are not implemented, as this is a base, abstract class."""

  knit_machine = knitting_plugin.BaseKnittingPlugin()
  with pytest.raises(NotImplementedError):
    knit_machine.configure()
  with pytest.raises(NotImplementedError):
    knit_machine.knit()
  with pytest.raises(NotImplementedError):
    knit_machine.finish()

def test_dummy_plugin():
  """Tests that dummy plugin flows as expected in ideal conditions."""
  knit_machine = dummy_plugin.DummyKnittingPlugin()
  knit_machine.configure(None)
  knit_machine.knit()
  knit_machine.finish()

def test_machine_handler_get_machines():
  for machine_type in list(machine_handler.get_machine_types()):
    assert machine_handler.get_machines_by_type(machine_type) == knitlib.plugins.active_plugins.get(machine_type, {})


def test_machine_handler_get_machine_by_id():
    machine = knitlib.machine_handler.get_machine_plugin_by_id("dummy")
    assert machine.__name__ == "DummyKnittingPlugin"

def test_dummy_machine():

    mach_type = knitlib.machine_handler.get_machine_types().other
    other_type_dict = knitlib.machine_handler.get_machines_by_type(mach_type)
    assert type(other_type_dict) is dict
    dummy_type = other_type_dict["dummy"]()

    dummy_type.configure(None)
    dummy_type.knit()
    dummy_type.finish()


def test_ayab_plugin():
    pass
    # machine = knitlib.machine_handler.get_machine_plugin_by_id("AYAB")()

    #dummy_type.configure(None)
    #dummy_type.knit() # https://bitbucket.org/chris007de/ayab-apparat/wiki/english/Hardware#!nomachine-development-mode
    #if dummy_type.isstate("finished"):
    #    dummy_type.finish()+
