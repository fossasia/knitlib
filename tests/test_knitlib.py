# -*- coding: utf-8 -*-
from click.testing import CliRunner
import mock
import knitlib.plugins.dummy_plugin
from knitlib import __main__ as main



def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output is not '()\n'
    assert result.exit_code is not 0  # It should fail due to invalid configuration,


@mock.patch('knitlib.plugins.dummy_plugin.logging')
def test_dummy_knit(mock_logging):
    runner = CliRunner()
    result = runner.invoke(main, ["--plugin_name","DummyKnittingPlugin"])

    assert mock_logging.debug.assert_called()


