__author__ = 'tian'

from knitlib.plugins.knitting_plugin import BaseKnittingPlugin
import uuid


class KnittingJob(object):
    """A Knitting job is composed of a Machine Plugin at a certain state, a port and a knitpat file."""

    def __init__(self, plugin_class, port, knitpat_dict):
        assert issubclass(plugin_class, BaseKnittingPlugin)
        self.id = uuid.uuid4()
        self.__plugin_class = plugin_class
        self.__plugin = None
        self.__port = port
        self.__knitpat_dict = knitpat_dict

    def get_plugin_name(self):
        return self.__plugin.__PLUGIN_NAME__

    def get_plugin_instance(self):
        return self.__plugin

    def get_status(self):
        return self.__plugin.current

    def start_job(self):
        self.__plugin = self.__plugin_class()
        assert self.__plugin.current == "activated"
        self.__plugin.set_port(self.__port)

    def configure_job(self):
        self.__plugin.configure(self.__knitpat_dict)

    def knit_job(self):
        # TODO: ensure plugin.knit is called asynchronously.
        self.__plugin.knit()
