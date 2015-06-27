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