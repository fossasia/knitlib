===============
Writing Plugins
===============

One of the main objectives of knitlib is to be a common platform for knitting machine software and control. Knitlib is
 designed with a modular approach, that allows programmers to easily create plugins without worrying about Control, UI
 elements, file and port abstractions, knitting pattern specification and format, etc.

Fundamental Abstractions: A Finite State Machine for Knitting Machines
======================================================================

Center to all abstractions in Knitlib is the Knitting Finite State Machine, defined at knitlib/plugins/knitting_plugin.py
BaseKnittingPlugin is a simple plugin base that offers several commodities for the handling of the knitting flow.
Function such as onconfigure, onknit and onfinish are used to setup the plugin and to operate it.


Documentation improvements
==========================

knitlib could always use more documentation, whether as part of the
official knitlib docs, in docstrings, or even on the web in blog posts,
articles, and such.
