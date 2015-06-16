
===============================
knitlib
===============================

.. | |docs| |travis| |appveyor| |coveralls| |landscape| |scrutinizer|
.. | |version| |downloads| |wheel| |supported-versions| |supported-implementations|

| |travis|


.. image:: https://badge.waffle.io/fashiontec/knitlib.png?label=ready&title=Ready
    :target: https://waffle.io/fashiontec/knitlib
    :alt: 'Stories in Ready'

.. # |docs| image:: https://readthedocs.org/projects/knitlib/badge/?style=flat
    :target: https://readthedocs.org/projects/knitlib
    :alt: Documentation Status

..  |travis| image:: http://img.shields.io/travis/fashiontec/knitlib/master.png?style=flat
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/fashiontec/knitlib

.. # |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/tian2992/knitlib?branch=master
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/tian2992/knitlib

.. # |coveralls| image:: http://img.shields.io/coveralls/tian2992/knitlib/master.png?style=flat
    :alt: Coverage Status
    :target: https://coveralls.io/r/tian2992/knitlib

.. # |landscape| image:: https://landscape.io/github/tian2992/knitlib/master/landscape.svg?style=flat
    :target: https://landscape.io/github/tian2992/knitlib/master
    :alt: Code Quality Status

.. # |version| image:: http://img.shields.io/pypi/v/knitlib.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/knitlib

.. # |downloads| image:: http://img.shields.io/pypi/dm/knitlib.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/knitlib

.. # |wheel| image:: https://pypip.in/wheel/knitlib/badge.png?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/knitlib

.. # |supported-versions| image:: https://pypip.in/py_versions/knitlib/badge.png?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/knitlib

.. # |supported-implementations| image:: https://pypip.in/implementation/knitlib/badge.png?style=flat
    :alt: Supported imlementations
    :target: https://pypi.python.org/pypi/knitlib

.. # |scrutinizer| image:: https://img.shields.io/scrutinizer/g/tian2992/knitlib/master.png?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/tian2992/knitlib/

A library designed to support the operation of varied knitting machines, mechanisms, and hacks.

Projects like Ayab and Knitic access knitting machines. The AYAB has already created a plugin system for knitting machines and implemented talking to Brother KH 910/930 models. The software is based on Python and QT. The primary task is to develop a library based on this solution to add support for more machines.

Free software: GPLv3+ license

Development Installation
========================

    pip install -r requirements.txt
    pip install knitlib

Documentation
=============

..  https://knitlib.readthedocs.org/

Development
===========

To run the all tests run::

    tox
