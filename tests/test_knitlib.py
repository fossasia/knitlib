
from click.testing import CliRunner
import knitlib
from knitlib.__main__ import main



def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output == '()\n'
    assert result.exit_code == 0

def test_machine_handler_get_machine_by_id():
    machine = knitlib.machine_handler.get_machine_by_id("DummyKnittingPlugin")
    assert machine.__name__ == "DummyKnittingPlugin"

def test_dummy_machine():

    mach_type = knitlib.machine_handler.get_machine_types().other
    other_type_dict = knitlib.machine_handler.get_machines_by_type(mach_type)
    assert type(other_type_dict) is dict
    dummy_type = other_type_dict["DummyKnittingPlugin"]()

    dummy_type.configure(None)
    dummy_type.knit()
    dummy_type.finish()


def test_ayab_plugin():
    machine = knitlib.machine_handler.get_machine_by_id("AyabPluginControl")()

    #dummy_type.configure(None)
    #dummy_type.knit() # https://bitbucket.org/chris007de/ayab-apparat/wiki/english/Hardware#!nomachine-development-mode
    #if dummy_type.isstate("finished"):
    #    dummy_type.finish()