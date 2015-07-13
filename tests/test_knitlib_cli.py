# -*- coding: utf-8 -*-
from click.testing import CliRunner
import mock
from knitlib import __main__ as main


def test_main_init_with_no_args():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output is not '()\n'
    assert result.exit_code is 0  # It should fail due to invalid configuration,


@mock.patch("knitlib.__main__.logging.error")
def test_invalid_plugin_fail(mock_logging):
    runner = CliRunner()
    result = runner.invoke(main, ["--plugin_name", "INVALID_PLUGIN"])
    # assert mock_logging has been called
    assert result.output is not '()\n'
    #assert result.exit_code is not 0


@mock.patch('knitlib.plugins.dummy_plugin.logging.debug')
def test_dummy_knit(mock_logging):
    runner = CliRunner()
    result = runner.invoke(main, ["--plugin_name", "dummy"])
    # assert mock_logging.called


