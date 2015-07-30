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

import sys
import click
import knitlib
import logging
import knitpat
# Why does this file exist, and why __main__?
# For more info, read:
# - https://www.python.org/dev/peps/pep-0338/
# - https://docs.python.org/2/using/cmdline.html#cmdoption-m
# - https://docs.python.org/3/using/cmdline.html#cmdoption-m

name = "knitlib"


@click.command()
@click.option('--plugin_name', default="dummy",  # pPluginType prompt='Name of the Machine Plugin you want.',
              help='The name of the Machine Plugin you want.')
@click.option('--config', multiple=True, nargs=2, type=click.Tuple([unicode, unicode]))
@click.option('--port', type=unicode)
def main(plugin_name, config, port):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Config got as object {0}".format(config))
    logging.debug("Port set as {}".format(port))
    config_dict = dict(config)
    logging.debug(config_dict)
    knitpat_dict = knitpat.parse_dict_from_cli(config_dict)
    logging.debug("Knitpat object parsed as object {0}".format(knitpat_dict))
    # Getting the selected plugin from ID.
    plugin = knitlib.machine_handler.get_machine_plugin_by_id(plugin_name)
    logging.debug("Plugin Selected: {0}".format(plugin))
    if plugin is None:
        print("The plugin selected is not available. Available plugins are: {}".
              format(knitlib.machine_handler.get_active_machine_plugins_names()))
        return -2
    machine_instance = plugin()
    machine_instance.configure(conf=knitpat_dict)
    machine_instance.knit()
    machine_instance.finish()
    return 0

if __name__ == "__main__":
    sys.exit(main())
