import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt5.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.animation import FuncAnimation
from itertools import count
from matplotlib.lines import Line2D


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
        self.combo_box = QComboBox()
        
        self.figure_f = None
        self.ax_f = None
        self.ax_d = None
        self.canvas_f = None
        self.canvas_d = None
        self.lines = []

        self.main_widget = self.__create_layouts()
        self.setCentralWidget(self.main_widget)
        self.animation = None



    def __create_layouts(self):
        """

        """
        # Create label and textbox for function, learning rate and start guess input
        text_title = QLabel("OPTIMIZATION PARAMETERS")
        input_label = QLabel("Function:")
        lr_label = QLabel("Learning Rate:")
        sg_label = QLabel("Starting Guess:")
        self.combo_box.addItem("Gradient Descent")
        self.combo_box.addItem("Stochastic Gradient Descent")
        self.combo_box.currentIndexChanged.connect(self.on_combobox_changed)


        # Create the generate button
        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self.generate_function_plot)
        generate_button.clicked.connect(self.generate_derivative_plot)
        
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

    
        title_layout = QHBoxLayout()
        title_layout.addWidget(text_title)
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
        merged_layout.addLayout(title_layout)
        merged_layout.addLayout(input_layout)
        merged_layout.addLayout(lr_layout)
        merged_layout.addLayout(sg_layout)
        merged_layout.addWidget(self.combo_box)
        merged_layout.addWidget(generate_button)

        # Create the main layout and add the widgets
        main_layout = QHBoxLayout()
        main_layout.addLayout(merged_layout)
        main_layout.addWidget(self.canvas_f)
        main_layout.addWidget(self.canvas_d)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)

        return main_widget

    def on_combobox_changed(self, index):
        selected_text = self.combo_box.currentText()
        selected_index = self.combo_box.currentIndex()
        print(f"Selected item: {selected_text} (index {selected_index})")
 

    def generate_function_plot(self):
        """

        """
        #selected_text = self.combo_box.currentText() for later
        try:
            temp_lr = float(self.lr_textbox.text())

        except ValueError as e:
              print(e)
              self.ax_f.clear()
              self.ax_f.set_title("Function")
              self.ax_f.text(0.5, 0.5, "Invalid learning rate", horizontalalignment='center', verticalalignment='center',
                                 transform=self.ax_f.transAxes)
              self.canvas_f.draw()
              return

        try:
            temp_guess = float(self.sg_textbox.text())

        except ValueError as e:
              print(e)
              self.ax_f.clear()
              self.ax_f.set_title("Function")
              self.ax_f.text(0.5, 0.5, "Invalid starting guess", horizontalalignment='center', verticalalignment='center',
                                 transform=self.ax_f.transAxes)
              self.canvas_f.draw()
              return

        self.lines = []
        self.stop_animation()
        self.ax_f.clear()
        self.canvas_f.draw()
        # Get the function string from the input box
        function_str = self.input_textbox.text()
        x_val = self.sg_textbox.text()
        x_val = float(x_val)

        if x_val < 0:
            x_min = x_val - 3
            x_max = -1 * x_val +3

        elif x_val >0:
            x_min = -1 * x_val -3
            x_max = x_val + 3

        else:
            x_min = -15
            x_max = 15

        # Define the range of x values
        x = np.linspace(x_min, x_max, 1000)
        
        # Evaluate the input function at each x value
        try:
            y = eval(function_str)
            f = lambda x: eval(function_str)
            df = lambda x:  eval(derivative(function_str))

        except (NameError, SyntaxError) as e:
              print(e)
              self.ax_f.clear()
              self.ax_f.set_title("Function")
              self.ax_f.text(0.5, 0.5, "Invalid Function", horizontalalignment='center', verticalalignment='center',
                                 transform=self.ax_f.transAxes)
              self.canvas_f.draw()
              return
        
        try:
            x_calc, y_calc = Gradient_Descent(guess=float(self.sg_textbox.text()), \
                    learning_rate = float(self.lr_textbox.text()), f=f, df=df)

        except OverflowError as e:
            self.ax_f.clear()
            self.ax_f.set_title("Function")
            self.ax_f.text(0.5, 0.5, "OverflowError. Try decreasing the learning rate.", horizontalalignment='center', verticalalignment='center',
                           transform=self.ax_f.transAxes)
            self.canvas_f.draw()
            return

        # Create a line object to draw the segments
        # Clear the plot and plot the new function
        self.ax_f.clear()
        self.ax_f.set_title("Function")
        self.ax_f.plot(x, y)
        self.canvas_f.draw()

        self.start_animation(x_calc, y_calc)


    def start_animation(self, x_calc, y_calc):
        """

        """
        self.animation = FuncAnimation(self.figure_f, self.animate, fargs=(x_calc, y_calc), frames=count())
        self.canvas_f.draw()


    def stop_animation(self):
        """

        """
        if self.animation is not None:
            self.animation.event_source.stop()


    def generate_derivative_plot(self):
        """

        """
        try:
            temp_lr = float(self.lr_textbox.text())

        except ValueError as e:
              print(e)
              self.ax_f.clear()
              self.ax_f.set_title("Function")
              self.ax_f.text(0.5, 0.5, "Invalid learning rate", horizontalalignment='center', verticalalignment='center',
                                 transform=self.ax_f.transAxes)
              self.canvas_f.draw()
              return

        try:
            temp_guess = float(self.sg_textbox.text())

        except ValueError as e:
              print(e)
              self.ax_f.clear()
              self.ax_f.set_title("Function")
              self.ax_f.text(0.5, 0.5, "Invalid starting guess", horizontalalignment='center', verticalalignment='center',
                                 transform=self.ax_f.transAxes)
              self.canvas_f.draw()
              return


        self.ax_d.clear()
        self.canvas_d.draw()
        # Get the function string from the input box
        function_str = self.input_textbox.text()
        
        x_val = self.sg_textbox.text()
        x_val = float(x_val)

        if x_val < 0:
            x_min = x_val - 3
            x_max = -1 * x_val +3

        elif x_val >0:
            x_min = -1 * x_val -3
            x_max = x_val + 3

        else:
            x_min = -15
            x_max = 15

        # Define the range of x values
        x = np.linspace(x_min, x_max, 1000)

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


    def animate(self,i, x_calc, y_calc):
        """

        """
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
                self.ax_f.add_line(line)
                self.lines.append(line)
            self.ax_f.plot(x_point, y_point, "--ro")
        
