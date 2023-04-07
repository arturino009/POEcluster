import uuid
from calculation_utils import NotableCombinationCalculator
import trade_api_utils
import gui_utils
import poe_db_utils
from PyQt5.QtWidgets import QApplication, QTableWidget
import time
from itertools import combinations
import os
import json
import sys
from PyQt5.QtCore import QThread

try:
    file_dir = "data/" + trade_api_utils.current_league
    if (os.path.exists(file_dir) == False):
        print("Didn't find data for current league. Updating...")
        poe_db_utils.updateClusterData()
    app = QApplication([])
    dialog = gui_utils.Dialog(file_dir)
    dialog.show()
    if dialog.exec_():
        resultList = dialog.result

    try:
        query = resultList[0]
    except NameError:
        sys.exit()
        
    dump_name = str(uuid.uuid4())
    inp = resultList[1]
    if query == 1:
        location = file_dir + "/small.json" if inp == 1 else file_dir + "/medium.json"
    else:
        location = file_dir + "/medium.json"

    all_cluster_jewels = list()
    # import all the data from file to memory
    with open(location) as json_file:
        all_cluster_jewels = json.load(json_file)

    selected_cluster_jewels = []
    for item in all_cluster_jewels:
        if item['clusterName'] in resultList:
            selected_cluster_jewels.append(item)

    # start the timer for program execution
    start_time = time.time()
    levelBreakpoints = [1,50,68,75]
    levelRequests = len(levelBreakpoints) * len(selected_cluster_jewels)
    notableRequests = 0

    if query == 2:
        for cluster_jewel in selected_cluster_jewels:
            notableRequests += cluster_jewel['clusterNotableCombinationCount']
    else:
        for cluster_jewel in selected_cluster_jewels:
            notableRequests += cluster_jewel['clusterNotableCount']

    print("Requests to make: " + str((levelRequests + notableRequests)))

    tableWidget = QTableWidget()
    tableWidget.show()

    calculator = NotableCombinationCalculator(selected_cluster_jewels, query,inp)
    workerThread = QThread()
    calculator.moveToThread(workerThread)

    # Connect the signals
    calculator.finished.connect(workerThread.quit)
    calculator.data_updated.connect(lambda data: gui_utils.display_table(tableWidget, data))

    workerThread.started.connect(calculator.process)

    workerThread.start()


    gui_utils.toggle_console(0)
    #print(all_averages)

    
    app.exec_()

except Exception as e:
    print(e)
    stop = int(input())
