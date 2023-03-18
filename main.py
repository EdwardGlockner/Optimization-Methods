import numpy as np
import matplotlib
import pylab
import pygame
from pygame.locals import *
#matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
from matplotlib import pyplot as plt
import os
import sys

# Fixing path
sys.path.append(str(sys.path[0][:-14]))
dirname = os.getcwd()
dirname = dirname.replace("", "")

from visualize import visualize_2D
from GD import Gradient_Descent

try:
    if sys.platform == "darwin": # macOS
        clear = lambda : os.system("clear")
    else:
        clear = lambda : os.system("cls")
except OSError as e:
    print("Could not identifiy operating systems")


def main():
    f = lambda x: x*x*x*x 
    df = lambda x:4*x*x*x 

    x_calc, y_calc = Gradient_Descent(guess = -9, \
            learning_rate = 0.0001, f = f, df = df)

    visualize_2D(f, -10, 10, x_calc, y_calc)

if __name__ == "__main__":
    main()
