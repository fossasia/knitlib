===============
Writing Plugins
===============

One of the main objectives of knitlib is to be a common platform for knitting machine software and control. Knitlib is
 designed with a modular approach, that allows programmers to easily create plugins without worrying about Control, UI
 elements, file and port abstractions, knitting pattern specification and format, etc.

Fundamental Abstractions: A Finite State Machine for Knitting Machines
======================================================================

Center to all abstractions in Knitlib is the Knitting Finite State Machine, defined at knitlib/plugins/knitting_plugin.py
