import sys
import click
import knitlib
import logging
# Why does this file exist, and why __main__?
# For more info, read:
# - https://www.python.org/dev/peps/pep-0338/
# - https://docs.python.org/2/using/cmdline.html#cmdoption-m
# - https://docs.python.org/3/using/cmdline.html#cmdoption-m


@click.command()
@click.option('--plugin_name', default="DummyKnittingPlugin",  # prompt='Name of the Machine Plugin you want.',
              help='The name of the Machine Plugin you want.')
@click.option('--config', multiple=True, nargs=2, type=click.Tuple([unicode, unicode]))
def main(plugin_name, config):
    logging.basicConfig(level=logging.DEBUG)
    config_dict = dict(config)
    logging.debug(config_dict)
    # Getting the selected plugin from ID.
    plugin = knitlib.machine_handler.get_machine_plugin_by_id(plugin_name)
    if plugin is None:
        logging.error("The plugin selected is not available. Available plugins are: {}".
                      format(knitlib.machine_handler.get_active_machine_plugins_names()))
        return -1
    machine_instance = plugin()
    machine_instance.configure(conf=config_dict)
    machine_instance.knit()
    machine_instance.finish()

if __name__ == "__main__":
    sys.exit(main())
