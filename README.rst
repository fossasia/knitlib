
===============================
knitlib
===============================

.. | |docs| |travis| |appveyor| |coveralls| |landscape| |scrutinizer|
.. | |version| |downloads| |wheel| |supported-versions| |supported-implementations|

| |travis| |docs| |downloads| |scrutinizer|


.. image:: https://badge.waffle.io/fashiontec/knitlib.png?label=ready&title=Ready
    :target: https://waffle.io/fashiontec/knitlib
    :alt: 'Stories in Ready'

..  |docs| image:: https://readthedocs.org/projects/knitlib/badge/?style=flat
    :target: https://readthedocs.org/projects/knitlib
    :alt: Documentation Status

..  |travis| image:: http://img.shields.io/travis/fashiontec/knitlib/master.png?style=flat
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/fashiontec/knitlib

..  |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/tian2992/knitlib?branch=master
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/tian2992/knitlib

..  |coveralls| image:: http://img.shields.io/coveralls/tian2992/knitlib/master.png?style=flat
    :alt: Coverage Status
    :target: https://coveralls.io/r/tian2992/knitlib

..  |landscape| image:: https://landscape.io/github/tian2992/knitlib/master/landscape.svg?style=flat
    :target: https://landscape.io/github/tian2992/knitlib/master
    :alt: Code Quality Status

..  |version| image:: http://img.shields.io/pypi/v/knitlib.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/knitlib

..  |downloads| image:: http://img.shields.io/pypi/dm/knitlib.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/knitlib

..  |wheel| image:: https://pypip.in/wheel/knitlib/badge.png?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/knitlib

..  |supported-versions| image:: https://pypip.in/py_versions/knitlib/badge.png?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/knitlib

.. |supported-implementations| image:: https://pypip.in/implementation/knitlib/badge.png?style=flat
    :alt: Supported imlementations
    :target: https://pypi.python.org/pypi/knitlib

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/tian2992/knitlib/master.png?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/tian2992/knitlib/
    
    
==================
1. What is Knitlib
==================
Knitlib is a library designed to support the operation of varied knitting machines, mechanisms, and hacks. Knitlib is based on projects like AYAB, PDD, and KnitterStream to control knitting machines. Knitlib features a plugin system for knitting machines and implements an API to control machines' operation, knitting jobs and knitting patterns. The software is based on Python. There also is a Web API. Among the primary tasks is to develop plugins based on this solution to add support for more machines.

1.1 Idea behind Knitlib
-----------------------

1.2 Technical Background of Knitlib
-----------------------------------

Knitlib is implemented as a Python Library and API. Each machine is supported via a Plugin, allowing for extensibility. Each of the plugins is based on a simple Finite State Machine, with states from machine initialization to operation and knitting process. Among the aplications using the Knitlib API is Knitlib-server, implementing a Webserver and REST / WebSocket endpoints. Clients can also implement message callbacks, errors, notifications and blocking messages in order to provide a good user experience.

==========================
2.Development Installation
==========================

    pip install -r requirements.txt
    pip install knitlib

========
3. Usage
========

==============
4. Development
==============

To run the all tests run::

    tox
    
=============
5. References
=============

================
6. Documentation
================

..  https://knitlib.readthedocs.org/

===============
7. Contributing
===============

7.1. Bug reports
----------------

Bugs can be reported via the Github issues tracker at https://github.com/fashiontec/knitlib/issues

7.2 Documentation improvements
------------------------------

7.3 Feature requests, Issues, and Feedback
-----------------------------------------------
Issues, feature requests and feedback can be reported via the Github issues tracker at https://github.com/fashiontec/knitlib/issues



7.4 Pull Request Guidelines
---------------------------



=============================
8. Applications using Knitlib
=============================

==========
9. License
==========

Free software: LGPLv3+ license
