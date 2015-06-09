
from click.testing import CliRunner
import knitlib
from knitlib.__main__ import main



def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output == '()\n'
    assert result.exit_code == 0


def test_getting_dummy_machine():

    mach_type = knitlib.machine_handler.get_machine_types().other
    other_type_dict = knitlib.machine_handler.get_machines_by_type(mach_type)
    assert type(other_type_dict) is dict
    dummy_type = other_type_dict["DummyKnittingPlugin"]()

    dummy_type.configure(None)
    dummy_type.knit()
    dummy_type.finish()

def test_ayab_plugin():
    mach_type = knitlib.machine_handler.get_machine_types().other
    other_type_dict = knitlib.machine_handler.get_machines_by_type(mach_type)
    assert type(other_type_dict) is dict
    dummy_type = other_type_dict["AyabPluginControl"]()

    dummy_type.configure(None)
    dummy_type.knit() # https://bitbucket.org/chris007de/ayab-apparat/wiki/english/Hardware#!nomachine-development-mode
    dummy_type.finish()