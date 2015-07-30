=====
Usage
=====

To use knitlib in a project::

	import knitlib

	# Search for a plugin via it's public name.
	Plugin = knitlib.machine_handler.get_machine_plugin_by_id(plugin_name)
	# Initalize the plugin instance
	machine_instance = Plugin()
	machine_instance.configure(conf={'options': 'go here'})
	# Knit will block execution. If you need async execution check the callbacks configuration.
	machine_instance.knit()
	machine_instance.finish()

Each machine has it's own configuration options, however the base functions are standardized in knitpat.
Check the Knitpat section for more info.

Knitlib API allows for setting callbacks for certain actions that the user needs to interact with the underlying
hardware. This callbacks system includes messaging, messages with blocking operations (move knob, set dial, feed yarn,
etc) and progress. Default callbacks are included for CLI operation, and projects should provide their own
implementations for the environment in use (knitweb, desktop UIs, etc).
