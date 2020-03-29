#!/usr/bin/env python3
"""Little application that will shrink a list of given jpg files to a desired size, set by user """

import os
import sys
from PIL import Image
from PyQt5 import QtWidgets
from interface import *


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    UI = Ui_MainWindow()
    UI.setupUi(MainWindow)
    QtWidgets.QApplication.setQuitOnLastWindowClosed(True)


def choosefiles():
    """
    After chooseButton is clicked, Function opens a FileDialog and lets you choose the *.jpg Files
    to work with from local storage. The selected files will be added to the global list FILE_NAMES
    """
    global FILE_NAMES
    FILE_NAMES = QtWidgets.QFileDialog.getOpenFileNames(
        filter="Bilddateien (*.jpg)")[0]
    UI.listWidget.addItems(FILE_NAMES[:])


def closeit():
    """
    Shut down the programm after closeButton is clicked
    """
    os._exit(1)


def compression():
    """Here the actual shrinking of the pictures takes place"""
    destinationfolder = QtWidgets.QFileDialog.getExistingDirectory()
    """
    When StartButton is clicked it will first open a Dialog, to choose the Destination Folder
    where the shrinked jpg's will be saved
    """
    percent = UI.verticalSlider.value()
    """
    percent holds the desired compression rate set by the slider in the GUI.
    100% is the initial value of the original File
    """

    # sets the initial value for the progressbar  to zero
    UI.progressBar.setValue(0)
    to_go = len(FILE_NAMES)  # number of files we want shrink.
    progr = 100 / to_go  # assign the progress after each file in percent to the  progressbar
    # progress,Initial value 1 to reach 100 in any case(rounding issues)
    completed = 1

    global choice
    choice = 0
    """choice holds the return value of the messagebox which pops up
       when the destination file already exists
    """

    for item in FILE_NAMES:
        """iteration cycle thrue the files in FILE_NAMES  """
        with open(item, 'rb') as file:
            picture = Image.open(file)
            xsize, ysize = picture.size
            xnew = xsize / 100 * percent
            ynew = ysize / 100 * percent
            height, width = int(ynew), int(xnew)
            """After opening file, calculation of desired picture size,
            outgoing from value set by slider
            """
            shrinked = picture.resize((width, height))
            head, tail = os.path.split(item)
            destination = destinationfolder + "/shrinked_" + tail
            """construction of the destination folder and filename"""
            if os.path.isfile(destination) and choice == 0:
                choice = show_popup()
            if os.path.isfile(destination) and choice == 262144:
                break
            if os.path.isfile(destination) and choice == 32768:
                os.remove(destination)
                """ control instance to handle file overwrite issues"""
            shrinked.save(destination)
            """ file is saved"""
            completed += progr
            UI.progressBar.setValue(completed)
            """ set updated value to progressbar"""


def clear_list():
    """ clearing the listWidget ande FILE_NAMES list so you can restart"""
    UI.listWidget.clear()
    FILE_NAMES.clear()


def show_popup():
    """Messagebox in case the file exists. Overwrite all or Abort """
    msg = QMessageBox()
    msg.setWindowTitle("File already exists")
    msg.setText("Same File(s) exists is Destination Folder! Overwrite?")
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.YesToAll | QMessageBox.Abort)
    msg.setDefaultButton(QMessageBox.YesToAll)
    msg.exec_()
    result = msg.result()
    return result


UI.chooseButton.clicked.connect(choosefiles)
UI.exitButton.clicked.connect(closeit)
UI.startButton.clicked.connect(compression)
UI.clearButton.clicked.connect(clear_list)
MainWindow.show()
sys.exit(app.exec_())
