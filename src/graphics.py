import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.animation import FuncAnimation
from itertools import count
from matplotlib.lines import Line2D


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
        
        self.figure_f = None
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
        self.figure_f = plt.figure(1)
        self.ax_f = self.figure_f.add_subplot(1,1,1)
        self.ax_f.set_xlabel('X')
        self.ax_f.set_ylabel('Y')
        self.ax_f.set_title("Function")
        self.canvas_f = FigureCanvas(self.figure_f)
        
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
        merged_layout.setSpacing(10)  # Adds 10 pixels of spacing between widgets
        merged_layout.setContentsMargins(30, 30, 30, 30)  # Adds 10 pixels of margins around the layout
        merged_layout.setAlignment(Qt.AlignCenter)  # Centers the widgets in the layout
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
        self.ax_f.clear()
        self.ax_d.clear()
        self.canvas_f.draw()
        self.canvas_d.draw()
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
            # Create a line object to draw the segments
            lines = []
            
            
            # Clear the plot and plot the new function
            self.ax_f.clear()
            self.ax_f.set_title("Function")
            self.ax_f.plot(x, y)
            self.canvas_f.draw()
            try:
                animation = FuncAnimation(self.figure_f, self.animate, fargs=(x_calc, y_calc, lines, self.ax_f, self.canvas_f), frames=count())
                self.canvas_f.draw()

            except Exception as e:
                for line in lines:
                    line.remove()
                # If there is an error, clear the plot and display an error message
                print(e)
                self.ax_f.clear()
                self.ax_f.set_title("Function")
                self.ax_f.text(0.5, 0.5, "Invalid Function", horizontalalignment='center', verticalalignment='center',
                             transform=self.ax_f.transAxes)
                self.canvas_f.draw()
                return

        except Exception as e:
            # If there is an error, clear the plot and display an error message
            print(e)
            self.ax_f.clear()
            self.ax_f.set_title("Function")
            self.ax_f.text(0.5, 0.5, "Invalid Function", horizontalalignment='center', verticalalignment='center',
                         transform=self.ax_f.transAxes)
            self.canvas_f.draw()
            return
        
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
            return


    def animate(self,i, x_calc, y_calc, lines, ax_f, canvas_f):
        if x_calc is None:
            for line in lines:
                line.remove()

            ax_f.clear()
            ax_f.set_title("Function")
            ax_f.text(0.5, 0.5, "Invalid Function", horizontalalignment='center', verticalalignment='center',
            transform=ax_f.transAxes)
            canvas_f.draw()
            return
        if i == len(x_calc) - 1:
            i = 0
            return 

        if i < len(x_calc):
            # Plot the next point in x_calc and y_calc
            x_point = x_calc[i]
            y_point = y_calc[i]
            if i > 0:
                # Add a line between the previous point and the current point
                x_prev = x_calc[i-1]
                y_prev = y_calc[i-1]
                line = Line2D([x_prev, x_point], [y_prev, y_point], color='r')
                ax_f.add_line(line)
                lines.append(line)
            ax_f.plot(x_point, y_point, "--ro")
        
        # Return a list of the artists that have been updated
        return [ax_f, *lines]
        
        """
        except Exception as e:
            for line in lines:
                line[0].remove()
            print("HERE1")
            self.ax_f.clear()
            self.ax_f.set_title("Function")
            self.ax_f.text(0.5, 0.5, "Invalid Function", horizontalalignment='center', verticalalignment='center',
                 transform=self.ax_f.transAxes)
            self.canvas_f.draw()

            return [self.ax_f, *lines]
        """



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
