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

Features
--------

The library supports two file formats

* `single file`: in this case the header is written at the beginnig of the file, which can be written and loaded from disk with two single calls.

* `sequential`: in this case the library creates a new temporary directory with two separate files, a header and a data file. This mode allows for sequential writing, e.g. when all the data to be written to disk is not known at once, but obtained through sequential calculations. The directory can be kept or brought into single file format very easily.


Authors
-------

Copyright (C) 2020, Mattia Bruno

Tutorials
---------

.. toctree::
   :maxdepth: 2

   tutorial1
   tutorial2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
