bison |release|
===============

A file format which combines the portability of JSON with the performance of binary IO.

The source code is hosted on `Github <https://github.com/mbruno46/bison>`__.

The philosophy
--------------


The file format is a combination of a header file written in JSON format, followed by streams of bytes.
The design of the package, written primarily for Python, has been driven by a few simple concepts:

* portability and human readability of the JSON format, 
  which allows to encode any structure, from simple 
  basic types, such as lists, to complex custom-defined classes.

* the performance of binary for large datasets contained in a `numpy.array`


The package is primarily designed for Python, but MATLAB/Octave interpreters will be added in future versions.

Authors
-------

Copyright (C) 2020, Mattia Bruno

Tutorials
---------

.. toctree::
   :maxdepth: 2

   tutorial1


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
