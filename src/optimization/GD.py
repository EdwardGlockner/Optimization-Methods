"""


"""
import numpy as np

def Gradient_Descent(guess, learning_rate, f, df, tolerance=1e-3, max_iters = 10000):
    """
    
    @params:
        guess:
        learning_rate:
        f:
        df:
        tolerance:
        max_iters:

    @returns:
        x_calc:
        y_calc:
    """

    if not callable(f):
        raise TypeError("Function 'f' must be callable")

    if not callable(df):
        raise TypeError("Gradient 'df' must be callable")

    if learning_rate <= 0:
        raise ValueError("Learning rate 'learning_rate' must be larger than zero")

    max_iters = int(max_iters)
    if max_iters <= 0:
        raise ValueError("Max iterations 'max_iters' must be larger than zero")

    if tolerance <= 0:
        raise ValueError("Tolerance 'tolerance' must be larger than zero")
    
    x_calc = []
    y_calc = []

    x_new = guess
    for _ in range(max_iters):
        # Save the calculated values
        x_calc.append(x_new)
        y_calc.append(f(x_new))
        step = -learning_rate * df(x_new)
                
        if np.abs(step) < tolerance:
            break
        x_new += step

    return x_calc, y_calc
