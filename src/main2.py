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
from derivative import derivative


try:
    if sys.platform == "darwin": # macOS
        clear = lambda : os.system("clear")
    else:
        clear = lambda : os.system("cls")
except OSError as e:
    print("Could not identifiy operating systems")


def main():
    equation = input("Enter function: ")
    
    f = lambda x: eval(equation)
    df = lambda x: eval(derivative(equation))

    x_calc, y_calc = Gradient_Descent(guess = 2.9, \
            learning_rate = 0.01, f = f, df = df)
    if x_calc is None or y_calc is None:
        return False

    visualize_2D(f, -3, 3, x_calc, y_calc)
    clear()

if __name__ == "__main__":

    clear()
    main()
