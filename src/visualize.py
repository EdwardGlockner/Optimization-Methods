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

    fig, ax = plt.subplots()
    ax.plot(x_cords, y_cords)
    ax.plot(x_calc, y_calc, "o")
    #plt.show()
    plt.draw()
    plt.pause(1)
    input("<Hit Enter To Close>")
    plt.close(fig)
    """
    plt.plot(x_cords, y_cords)
    plt.plot(x_calc, y_calc, "o")
    plt.show()
    """

