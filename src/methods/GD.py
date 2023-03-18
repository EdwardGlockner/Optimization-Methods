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
    x_calc = []
    y_calc = []

    x_new = guess
    for _ in range(max_iters):
        # Save the calculated values
        x_calc.append(x_new)
        y_calc.append(f(x_new))
    
        # Take new step
        step = -learning_rate * df(x_new)
                
        if np.abs(step) < tolerance:
            break

        x_new += step

    return x_calc, y_calc
