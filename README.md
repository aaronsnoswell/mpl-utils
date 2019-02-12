# mpl-utils

A collection of plotting functions for Matplotlib

# Functions

## thead_plot.py: Thread Plot

A plot designed for visualising large matrices or vectors.
Each row of the matrix is rendered as a spline-interpolated line, allowing 
structure in the matrix to be quickly visualised:

![Thread plot example image](figures\thread_plot.png)

# Installation

This package is not distributed on PyPI - you'll need to install it from source:

```bash
$> git clone github.com/aaronsnoswell/mpl-utils
$> cd mpl-utils
$> pip install -e .
```

To test the installation:

```bash
$> cd ~
$> python
$> from mpl_utils import *
```
