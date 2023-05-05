import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton


#---Fixing Path-----------------+
sys.path.append(str(sys.path[0][:-14]))
dirname = os.getcwd()
dirname = dirname.replace("src/", "")
sys.path.insert(1, os.path.join(dirname, "src/methods"))


#---Local Imports---------------+
from optimization.GD import Gradient_Descent
from optimization.SGD import Stoch_Gradient_Descent
from derivative import derivative


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Function Plotter")
        self.setGeometry(100, 100, 1600, 700)
        
        self.input_textbox = QLineEdit()
        self.lr_textbox = QLineEdit()
        self.sg_textbox = QLineEdit()

        self.ax_f = None
        self.ax_d = None
        self.canvas_f = None
        self.canvas_d = None

        self.main_widget = self.__create_layouts()
        self.setCentralWidget(self.main_widget)



    def __create_layouts(self):
        # Create label and textbox for function, learning rate and start guess input
        input_label = QLabel("Function:")
        lr_label = QLabel("Learning Rate:")
        sg_label = QLabel("Starting Guess:")

        # Create the generate button
        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self.generate_plot)
        
        # Create the plot canvas for the function
        figure_f = plt.figure(1)
        self.ax_f = figure_f.add_subplot(1,1,1)
        self.ax_f.set_xlabel('X')
        self.ax_f.set_ylabel('Y')
        self.ax_f.set_title("Function")
        self.canvas_f = FigureCanvas(figure_f)
        
        # Create the plot canvas for the derivative
        figure_d = plt.figure(2)
        self.ax_d = figure_d.add_subplot(1,1,1)
        self.ax_d.set_xlabel('X')
        self.ax_d.set_ylabel('Y')
        self.ax_d.set_title("Derivative")
        self.canvas_d = FigureCanvas(figure_d)

        # Create the layout for the input widget
        input_layout = QHBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_textbox)
        
        # Create the layout for the learning rate widget
        lr_layout = QHBoxLayout()
        lr_layout.addWidget(lr_label)
        lr_layout.addWidget(self.lr_textbox)

        # Create the layout for the starting guess widget
        sg_layout = QHBoxLayout()
        sg_layout.addWidget(sg_label)
        sg_layout.addWidget(self.sg_textbox)

        # Merge the three layouts
        merged_layout = QVBoxLayout()
        merged_layout.addLayout(input_layout)
        merged_layout.addLayout(lr_layout)
        merged_layout.addLayout(sg_layout)
        merged_layout.addWidget(generate_button)

        # Create the main layout and add the widgets
        main_layout = QHBoxLayout()
        main_layout.addLayout(merged_layout)
        main_layout.addWidget(self.canvas_f)
        main_layout.addWidget(self.canvas_d)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)

        return main_widget
 

    def f(self, equation):
        return eval(equation)


    def df(self, equation):
        return eval(derivative(equation))


    def generate_plot(self):
        # Get the function string from the input box
        function_str = self.input_textbox.text()

        # Define the range of x values
        x = np.linspace(-15, 15, 1000)

        try:
            # Evaluate the input function at each x value
            y = eval(function_str)

            f = lambda x: eval(function_str)
            df = lambda x:  eval(derivative(function_str))
            x_calc, y_calc = Gradient_Descent(guess=float(self.sg_textbox.text()), \
                    learning_rate = float(self.lr_textbox.text()), f=f, df=df)
            
            # Clear the plot and plot the new function
            self.ax_f.clear()
            self.ax_f.set_title("Function")
            self.ax_f.plot(x, y)
            self.ax_f.plot(x_calc, y_calc, "--ro")
            self.canvas_f.draw()
        except:
            # If there is an error, clear the plot and display an error message
            self.ax_f.clear()
            self.ax_f.set_title("Function")
            self.ax_f.text(0.5, 0.5, "Invalid Function", horizontalalignment='center', verticalalignment='center',
                         transform=self.ax_f.transAxes)
            self.canvas_f.draw()
        
        try:
            y_d = eval(derivative(function_str))
            self.ax_d.clear()
            self.ax_d.set_title("Derivative")
            self.ax_d.plot(x,y_d)
            self.canvas_d.draw()
        except:
            self.ax_d.clear()
            self.ax_d.set_title("Derivative")
            self.ax_d.text(0.5, 0.5, "Invalid Function", horizontalalignment='center', verticalalignment='center',
                           transform=self.ax_d.transAxes)
            self.canvas_d.draw()



# Get the domain of the function
def get_function_domain(function):
    # Parse the function to get the variable name
    var_name = function.split('=')[0].strip()

    # Evaluate the function for a range of x values
    x_values = np.linspace(-10, 10, 1000)
    y_values = np.array([eval(function) for x in x_values])

    # Find the first and last non-NaN values
    idx_min = np.argmax(np.isfinite(y_values))
    idx_max = len(y_values) - np.argmax(np.isfinite(y_values[::-1])) - 1

    # Return the domain of the function
    return x_values[idx_min], x_values[idx_max]
