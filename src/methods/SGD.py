"""


"""
import numpy as np

def Stoch_Gradient_Descent(guess, learning_rate, f, df, tolerance=1e-3, max_iters = 10000, batch_size = 1, random_state = None):
    """

    @params:
        guess:
        learning_rate:
        f:
        df:
        tolerance:
        max_iters:
        batch_size:
        random_state:
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

    batch_size = int(batch_size)
    if not 0 < batch_size:
        raise ValueError("Batch size 'batch_size' must be larger than zero")

    x_calc = []
    y_calc = []

    seed = None if random_state is None else int(random_state)
    rng = np.random.default_rng(seed=seed)
    
    return x_calc, y_calc
