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


import abc
import logging
from fysom import Fysom


class BaseKnittingPlugin(Fysom):
    """A generic plugin implementing a state machine for knitting.

    Subclasses inherit the basic State Machine defined in __init__.
    """

    @abc.abstractmethod
    def onknit(self, e):
        """Callback when state machine executes knit().

        Starts the knitting process, this is the only function call that can block indefinitely, as it is called from an instance
        of an individual Thread, allowing for processes that require timing and/or blocking behaviour.
        """
        raise NotImplementedError(
            self.__NOT_IMPLEMENTED_ERROR.format("onknit. It is used for the main 'knitting loop'."))

    @abc.abstractmethod
    def onfinish(self, e):
        """Callback when state machine executes finish().

        When finish() gets called, the plugin is expected to be able to restore it's state back when configure() gets called.
        Finish should trigger a Process Completed notification so the user can operate accordingly.
        """
        raise NotImplementedError(
            self.__NOT_IMPLEMENTED_ERROR.format("onfinish. It is a callback that is called when knitting is over."))

    @abc.abstractmethod
    def onconfigure(self, e):
        """Callback when state machine executes configure(options={})

        This state gets called to configure the plugin for knitting. It can either
        be called when first configuring the plugin, when an error happened and a
        reset is necessary.

        Args:
          options: An object holding an options dict.
        """
        raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format(
            "onconfigure. It is used to configure the knitting plugin before starting."))

    @abc.abstractmethod
    def publish_options(self):
        raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format(
            "publish_options must be defined. It is used to expose the possible knitting options."))

    @abc.abstractmethod
    def validate_configuration(self, conf):
        raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format(
            "validate_configuration must be defined. It verifies configurations are valid."))

    @abc.abstractmethod
    def set_port(self, port_name):
        """Sets a port name before configuration method."""

    def register_interactive_callbacks(self, callbacks=None):
        """Serves to register a dict of callbacks that require interaction by the User,

         Interactive callbacks serve to block operation until a human acts on them. Interactive callbacks can include
         physical operations (set needles, move knob, flip switch), decisions (yes/no or cancel), or simply human
         acknowledgement.

         Args:
            callbacks: keys can be info, warning, progress, error.

         """
        if callbacks is None:
            callbacks = {}
        self.interactive_callbacks = callbacks

    @staticmethod
    def __cli_emit_message(message, level="info"):
        # TODO: use appropriate logging level for message.
        logging.info(message)

    @staticmethod
    def __cli_blocking_action(message, level="info"):
        """Capturing raw_input to block CLI action."""
        # TODO: use appropriate logging level for message.
        logging.info(message)
        raw_input()

    @staticmethod
    def __cli_log_progress(percent, done, total):
        """Logs progress percentage and lines of current job."""
        logging.info("Knitting at {}% . {} out of {}.".format(percent, done, total))

    def __init__(self, callbacks_dict=None, interactive_callbacks=None):
        self.__NOT_IMPLEMENTED_ERROR = "Classes that inherit from KnittingPlugin should implement {0}"
        """Interactive callbacks handle Plugin-Frontend interaction hooks."""
        self.interactive_callbacks = {}

        # Are we running on CLI or knitlib web?
        # If no callbacks are registered, we set a CLI set as default.
        if interactive_callbacks is None:
            self.register_interactive_callbacks({
                "blocking_user_action": BaseKnittingPlugin.__cli_blocking_action,
                "message": BaseKnittingPlugin.__cli_emit_message,
                "progress": BaseKnittingPlugin.__cli_log_progress
            })
        else:
            self.register_interactive_callbacks(interactive_callbacks)

        # Fysom allows to set hooks before changing states, we set them here.
        if callbacks_dict is None:
            callbacks_dict = {
                'onknit': self.onknit,
                'onconfigure': self.onconfigure,
                'onfinish': self.onfinish,
            }
        Fysom.__init__(self, {
            'initial': 'activated',
            'events': [  # TODO: add more states for handling error management.
                         {'name': 'configure', 'src': 'activated', 'dst': 'configured'},
                         {'name': 'configure', 'src': 'configured', 'dst': 'configured'},
                         {'name': 'configure', 'src': 'finished', 'dst': 'configured'},
                         {'name': 'configure', 'src': 'error', 'dst': 'configured'},
                         {'name': 'knit', 'src': 'configured', 'dst': 'knitting'},
                         {'name': 'finish', 'src': 'knitting', 'dst': 'finished'},
                         {'name': 'finish', 'src': 'finished', 'dst': 'finished'},
                         {'name': 'fail', 'src': 'knitting', 'dst': 'error'}],
            'callbacks': callbacks_dict
        })
