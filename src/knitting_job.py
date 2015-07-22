__author__ = 'tian'

from knitlib.plugins.knitting_plugin import BaseKnittingPlugin


class KnittingJob(object):
    """A Knitting job is composed of a Machine Plugin at a certain state, a port and a knitpat file."""

    def __init__(self, plugin_class, port, knitpat_file):
        assert issubclass(plugin_class, BaseKnittingPlugin)
        self.__plugin_class = plugin_class
        self.__plugin = None
        self.__port = port
        self.__knitpat_file = knitpat_file

    def get_plugin_name(self):
        return self.__plugin.__PLUGIN_NAME__

    def start_job(self):
        # TODO: send port info to plugin class.
        self.__plugin = self.__plugin_class()
        assert self.__plugin.current == "activated"

    def configure_job(self):
        self.__plugin.configure(self.__knitpat_file)

    def knit_job(self):
        # TODO: ensure plugin.knit is called asynchronously.
        self.__plugin.knit()
