from matplotlib import pyplot as plt



def visualize_2D(f, x_min, x_max, x_calc, y_calc):
    """
    @params:
        f: function
        x_min:
        x_mac:
        x_calc:
        y_calc:
    """
    x_cords = range(x_min, x_max)
    y_cords = [f(i) for i in x_cords]
    plt.plot(x_cords, y_cords)
    plt.plot(x_calc, y_calc, "o")
    plt.show()
