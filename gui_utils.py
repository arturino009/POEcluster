
import ctypes
import json
import os
import webbrowser
import trade_api_utils
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


def dump_data(dump_name, data):
    file_dir = "data/dump"
    if (os.path.exists("data") == False):
        os.mkdir("data")
    if (os.path.exists(file_dir) == False):
        os.mkdir(file_dir)

    with open(file_dir + '/'+ dump_name + '.json', 'w') as outfile:
        json.dump(data, outfile)

def toggle_console(a):
    # hiding the console
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW_HIDE = a
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, SW_HIDE)


def open_link(q):
    id = q.id
    webbrowser.open('https://www.pathofexile.com/trade/search/' +
                    trade_api_utils.current_league + '/' + id)

def display_table(tableWidget, data):
    keys_to_remove = ["request", "category_full", "notable_full"]
    for item in data:
        for key in keys_to_remove:
            if key in item:
                del item[key]

    row_count = len(data)
    column_count = len(data[0])

    tableWidget.setColumnCount(column_count) 
    tableWidget.setRowCount(row_count)
    tableWidget.setHorizontalHeaderLabels((list(data[0].keys())))
    for row in range(row_count):  # add items from array to QTableWidget
        for column in range(column_count):
            item = QTableWidgetItem()
            item.id = list(data[row].values())[11]
            item.setData(Qt.EditRole, (list(data[row].values())[column]))
            tableWidget.setItem(row, column, item)
    tableWidget.setColumnHidden(11, True)
    tableWidget.setSortingEnabled(True)
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tableWidget.itemDoubleClicked.connect(open_link)

class Dialog(QDialog):
    file_dir = ""

    def __init__(self, file_dir, parent=None):
        super(Dialog, self).__init__(parent)

        self.file_dir = file_dir

        layout = QGridLayout()
        self.setLayout(layout)

        countbutton1 = QRadioButton("Single notable")
        countbutton1.setChecked(True)
        countbutton1.type = 1
        countbutton1.layout = layout
        layout.addWidget(countbutton1, 0, 0)

        countbutton2 = QRadioButton("Double notable")
        # radiobutton.setChecked(True)
        countbutton2.type = 0
        countbutton2.layout = layout
        layout.addWidget(countbutton2, 0, 1)

        clustersizebutton1 = QRadioButton("Small cluster jewels")
        # radiobutton.setChecked(True)
        clustersizebutton1.type = 1
        clustersizebutton1.layout = layout
        clustersizebutton1.toggled.connect(self.onClicked)
        layout.addWidget(clustersizebutton1, 1, 0)

        clustersizebutton2 = QRadioButton("Medium cluster jewels")
        clustersizebutton2.type = 0
        clustersizebutton2.layout = layout
        clustersizebutton2.toggled.connect(self.onClicked)
        layout.addWidget(clustersizebutton2, 1, 1)

        self.btngroup1 = QButtonGroup()
        self.btngroup2 = QButtonGroup()

        self.btngroup1.addButton(countbutton1)
        self.btngroup1.addButton(countbutton2)
        self.btngroup2.addButton(clustersizebutton1)
        self.btngroup2.addButton(clustersizebutton2)

    def deleteAllWidgetsUntil(self, a):
        layout = self.layout
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)
            if i == a:
                break

    def onClicked(self):
        clustersizebutton = self.sender()
        layout = clustersizebutton.layout
        if clustersizebutton.type == 1:
            location = self.file_dir + "/small.json"
        else:
            location = self.file_dir + "/medium.json"
        with open(location) as json_file:
            all_lists = json.load(json_file)
        count = 1
        if layout.count() > 4:
            self.layout = layout
            self.deleteAllWidgetsUntil(4)
        for category in all_lists:
            count += 1
            clusterbox = QCheckBox(category['clusterName'])
            clusterbox.setChecked(False)
            clusterbox.type = category['clusterName']
            layout.addWidget(clusterbox, count, 0)
        executebutton = QPushButton("Execute")
        executebutton.layout = layout
        executebutton.clicked.connect(self.onExecute)
        layout.addWidget(executebutton, layout.count(), 0)
    def onExecute(self):
        button = self.sender()
        layout = button.layout
        if layout.itemAt(1).widget().isChecked() and layout.itemAt(2).widget().isChecked():
            print("Can't get double notables for small cluster jewels!")
            return
        result = []
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget.isChecked():
                result.append(widget.type)
        if len(result) == 2: 
            print("No categories selected!")
            return
        self.result =  result
        self.accept()
