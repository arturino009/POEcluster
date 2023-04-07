
import gui_utils
from PyQt5.QtWidgets import QApplication, QTableWidget
import json
import os


def get_most_recent_dump():
    file_dir = "data/dump"
    if (os.path.exists("data") == False):
        os.mkdir("data")
    if (os.path.exists(file_dir) == False):
        os.mkdir(file_dir)
    files = os.listdir(file_dir)
    files.sort(key=lambda x: os.path.getmtime(file_dir + "/" + x))
    return files[-1]

# display the most recent dump
app = QApplication([])
data = json.load(open("data/dump/" + get_most_recent_dump()))
tableWidget = QTableWidget()
tableWidget.show()
gui_utils.display_table(tableWidget, data)
app.exec_()