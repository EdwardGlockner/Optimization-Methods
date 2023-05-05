#---Imports---------------------+
import os
import sys
from PyQt5.QtWidgets import QApplication


#---Fixing Path-----------------+
sys.path.append(str(sys.path[0][:-14]))
dirname = os.getcwd()
dirname = dirname.replace("src/", "")
sys.path.insert(1, os.path.join(dirname, "src/methods"))


#---Local Imports---------------+
from graphics import MainWindow
from optimization.GD import Gradient_Descent
from optimization.SGD import Stoch_Gradient_Descent
from derivative import derivative


#---Main------------------------+
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


#---Run Code--------------------+
if __name__ == "__main__":
    main()
