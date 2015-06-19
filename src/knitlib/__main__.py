import sys
import click
import knitlib
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
    plugin = knitlib.machine_handler.get_machine_plugin_by_id(plugin_name)
    machine_instance = plugin()
    machine_instance.configure(dict(config))
    machine_instance.knit()
    machine_instance.finish()

if __name__ == "__main__":
    sys.exit(main())
