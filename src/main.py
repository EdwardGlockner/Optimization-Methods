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
#dirname = dirname.replace("", "")
sys.path.insert(1, os.path.join(dirname, "methods"))
from visualize import visualize_2D
from GD import Gradient_Descent
from SGD import Stoch_Gradient_Descent


try:
    if sys.platform == "darwin": # macOS
        clear = lambda : os.system("clear")
    else:
        clear = lambda : os.system("cls")
except OSError as e:
    print("Could not identifiy operating systems")


def main():
    #f = lambda x: x**4 - 5*x**2 - 3*x
    #df = lambda x: 4 * x**3 - 10 * x - 3

    #f = lambda x: x**2
    #df = lambda x: 2*x

    equation = input("Enter function: ")
    dequation = input("Enter gradient of function: ")
    
    f = lambda x: eval(equation)
    df = lambda x: eval(dequation)

    x_calc, y_calc = Gradient_Descent(guess = 2.9, \
            learning_rate = 0.9, f = f, df = df)

    visualize_2D(f, -3, 3, x_calc, y_calc)
    clear()

if __name__ == "__main__":

    clear()
    main()
