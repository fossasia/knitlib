# knitlib

A library designed to support the operation of varied knitting machines, mechanisms, and hacks.

Knitlib is based on projects like AYAB, PDD, and KnitterStream to control knitting machines. Knitlib features a plugin system for knitting machines and implements an API to control machines' operation, knitting jobs and knitting patterns. The software is based on Python. There also is a Web API defined in knitlib_webserver. Among the primary objectives is to develop plugins based on this solution to add support for more machines.

Free software: GPLv3+ license

## Development Installation

    pip install -r requirements.txt
    pip install knitlib

## Documentation

Detailed API documentation is available at https://readthedocs.org/projects/knitlib/

## Development

To run the all tests, use tox:

    tox
