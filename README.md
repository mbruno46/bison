
![Build Doc](https://github.com/mbruno46/bison/workflows/Build%20Doc/badge.svg)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

# bison - BInary jSON

A file format which combines the portability of JSON with the performance of binary IO.

- **Website:** https://mbruno46.github.io/bison/
- **Documentation:** https://mbruno46.github.io/bison/
- **Examples:** [tests](./tests)
- **Source code:** https://github.com/mbruno46/bison/
- **Bug reports:** https://github.com/mbruno46/bison/issues

### The philosophy

The file format is a combination of a header file written in JSON format, followed by streams of bytes.
The design of the package, written primarily for Python, has been driven by a few simple concepts:

 * portability and human readability of the JSON format, which allows to encode any structure, from simple 
 basic types, such as lists, to complex custom-defined classes.
 
 * the performance of binary for large datasets contained in a `numpy.array`
 
The package is primarily designed for Python, but MATLAB/Octave interpreters will be added in future versions.

### Authors

Copyright (C) 2020, Mattia Bruno

## Installation

The latest version of the package can be installed using `pip` directly from the github server

```bash
pip install git+https://github.com/mbruno46/bison.git@main
```

or after downloading the git repository

```bash
git clone git@github.com:mbruno46/bison.git
cd bison
pip install .
```

Alternatively, since no precompilation is needed, one can simply add the package to the path

```python
import sys
sys.path.append('path/to/bison')
import bison
```

## Example

```python
import numpy
import bison

db = {'name': 'Mattia', 'id': 0}
indices = [0,56,89,3,-45]
shape = (4,5,6)
array = numpy.arange(456).reshape(shape)

bison.save('full.dat',db,indices,shape,array)

bison.save('db.dat',db)

bison.save('array.dat',array,shape)

_array = bison.load('array.dat')
```
