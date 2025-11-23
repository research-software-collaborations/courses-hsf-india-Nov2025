import numpy as np
from mandelbrot_numpy import mandelbrot_numpy

# remember the patch position ij
def task(x, y, ij):
    return mandelbrot_numpy(x, y), ij
