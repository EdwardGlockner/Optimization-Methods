import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create the input field and button
        self.function_label = QLabel("Enter Function:")
        self.function_input = QLineEdit()
        self.generate_button = QPushButton("Generate Plot")

        # Add the widgets to the layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.function_label)
        self.layout.addWidget(self.function_input)
        self.layout.addWidget(self.generate_button)

        # Set the layout
        self.setLayout(self.layout)

        # Connect the button to the plot generation function
        self.generate_button.clicked.connect(self.generate_plot)

    def generate_plot(self):
        # Get the function input
        function_str = self.function_input.text()

        # Create an array of x values
        x = np.linspace(-10, 10, 1000)

        # Evaluate the function at each x value
        try:
            y = eval(function_str)(x)
        except:
            # Show an error message if the function is invalid
            self.error_dialog = QLabel("Invalid Function")
            self.error_dialog.show()
            return

        # Create the plot
        plt.plot(x, y)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Function Plot")
        plt.show()

if __name__ == "__main__":
    # Create the application and window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Run the event loop
    sys.exit(app.exec_())
