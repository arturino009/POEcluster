from updateClusterData import updateClusterData
import priceGetter
import time
from itertools import combinations
import webbrowser
import os
import json
import ctypes
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

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
                    priceGetter.current_league + '/' + id)

class Dialog(QDialog):
    def __init__(self, file_dir, parent=None):
        super(Dialog, self).__init__(parent)
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
            location = file_dir + "/small.json"
        else:
            location = file_dir + "/medium.json"
        with open(location) as json_file:
            all_lists = json.load(json_file)
        count = 1
        if layout.count() > 4:
            self.layout = layout
            self.deleteAllWidgetsUntil(4)
        for category in all_lists:
            count += 1
            clusterbox = QCheckBox(category['clusterName'])
            clusterbox.setChecked(True)
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


try:
    file_dir = "data/" + priceGetter.current_league
    if (os.path.exists(file_dir) == False):
        print("Didn't find data for current league. Updating...")
        updateClusterData()
    app = QApplication([])
    dialog = Dialog(file_dir)
    dialog.show()
    if dialog.exec_():
        resultList = dialog.result

    try:
        query = resultList[0]
    except NameError:
        quit()
    inp = resultList[1]
    if query == 1:
        location = file_dir + "/small.json" if inp == 1 else file_dir + "/medium.json"
    else:
        location = file_dir + "/medium.json"

    all_lists = list()
    # import all the data from file to memory
    with open(location) as json_file:
        all_lists = json.load(json_file)

    finalfinallist = []
    for item in all_lists:
        if item['clusterName'] in resultList:
            finalfinallist.append(item)
    all_lists = finalfinallist
    # start the timer for program execution
    start_time = time.time()
    levelBreakpoints = [1,50,68,75]
    levelRequests = len(levelBreakpoints) * len(all_lists)
    notableRequests = 0

    if query == 2:
        for a in all_lists:
            notableRequests += a['clusterNotableCombinationCount']
    else:
        for a in all_lists:
            notableRequests += a['clusterNotableCount']

    print("Requests to make: " + str((levelRequests + notableRequests)))

    # list of all values that I will get
    all_averages = list()
    for a in all_lists:
        if query == 1:
            comb = a['clusterNotables']
        else:
            # make a list of all possible combinations of items in each category
            comb = list(combinations(a['clusterNotables'], 2))
        lvlPrice = list()
        for lvl in levelBreakpoints:
            x = {
                'lvl': lvl,
                'price': priceGetter.get_category_jewel_price(a, lvl)
            }
            lvlPrice.append(x)
        a['breakpointPrices'] = lvlPrice
        for b in comb:
            if query == 1:
                min_lvl = b['notableLevel']
            else:
                seq = [x['notableLevel'] for x in b]
                min_lvl = max(seq)
            for item in a['breakpointPrices']:
                if item['lvl'] == min_lvl:
                    jewel_price = item['price']
                    break
            notableData = priceGetter.getNotablePrice(a, b, query, inp, jewel_price)
            if notableData != 0:
                all_averages.append(notableData)

    toggle_console(0)
    #print(all_averages)

    keys_to_remove = ["request", "category_full", "notable_full"]
    for item in all_averages:
        for key in keys_to_remove:
            del item[key]

    tableWidget = QTableWidget()
    row_count = len(all_averages)
    column_count = len(all_averages[0])

    tableWidget.setColumnCount(column_count) 
    tableWidget.setRowCount(row_count)
    tableWidget.setHorizontalHeaderLabels((list(all_averages[0].keys())))
    for row in range(row_count):  # add items from array to QTableWidget
        for column in range(column_count):
            item = QTableWidgetItem()
            item.id = list(all_averages[row].values())[11]
            item.setData(Qt.EditRole, (list(all_averages[row].values())[column]))
            tableWidget.setItem(row, column, item)
    tableWidget.setColumnHidden(11, True)
    tableWidget.setSortingEnabled(True)
    tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tableWidget.itemDoubleClicked.connect(open_link)
    tableWidget.show()
    app.exec_()

except Exception as e:
    print(e)
    stop = int(input())