"""


"""

def Gradient_Descent(guess, learning_rate, f, df, precision = 0.00001, max_iters = 10000):
    """
    @params:
        guess:
        learning_rate:
        precision:
        max_iters:
        f:
        df:

    @returns:


    """
    iters = 0
    x_calc = []
    y_calc = []
    step_size = 10
    
    new_x = guess
    while step_size > precision and iters < max_iters:
        old_x = new_x
        print(old_x)
        x_calc.append(old_x)
        y_calc.append(f(old_x))
        new_x = new_x - learning_rate * df(old_x)
        step_size = abs(new_x - old_x)
        iters += 1

    return x_calc, y_calc

    

