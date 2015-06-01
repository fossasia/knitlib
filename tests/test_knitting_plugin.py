
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
    knit_machine.knit()
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

