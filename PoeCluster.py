from updateClusterData import updateClusterData
import priceGetter
import requests
import time
from itertools import combinations
from tkinter import *
from TkTreectrl import *
import webbrowser
import os
import json
import ctypes
import sys


def toggle_console(a):
    # hiding the console
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW_HIDE = a
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, SW_HIDE)


def open_link(q):
    webbrowser.open('https://www.pathofexile.com/trade/search/' +
                    priceGetter.current_league + '/' + all_averages[q]['id'])


def sort_items(sort_type):
    global all_averages
    all_averages = sorted(
        all_averages, key=lambda i: i[sort_type], reverse=True)
    refreshList()


def update():
    toggle_console(1)
    try:
        a = treeview.curselection()[0]
    except:
        return
    all_averages[a] = priceGetter.getNotablePrice(
        all_averages[a]['category_full'], all_averages[a]['notable_full'], query, inp)
    refreshList()
    toggle_console(0)


def refreshList():
    treeview.delete(ALL)
    for item in all_averages:
        treeview.insert(END, item['name'], item['listings'], item['tries'], item['craft'], item['first'],
                        item['average'], item['profit'], item['PPT'], item['LPPT'], item['ilvl'], item['category'])


try:
    file_dir = "data/" + priceGetter.current_league
    if (os.path.exists(file_dir) == False):
        print("Didn't find data for current league. Updating...")
        updateClusterData()


    print('Input 1 for single notable prices, 2 for double notable prices.')
    query = int(input())
    inp = 0
    if query == 1:
        print('Input 1 to check small cluster jewels, 2 for medium cluster jewels.')
        inp = int(input())
        location = file_dir + "/small.json" if inp == 1 else file_dir + "/medium.json"
    else:
        location = file_dir + "/medium.json"

    all_lists = list()
    # import all the data from file to memory
    with open(location) as json_file:
        all_lists = json.load(json_file)

    # start the timer for program execution
    start_time = time.time()

    # list of all values that I will get
    all_averages = list()
    for a in all_lists:
        if query == 1:
            comb = a['clusterNotables']
        else:
            # make a list of all possible combinations of items in each category
            comb = list(combinations(a['clusterNotables'], 2))
        for b in comb:
            notableData = priceGetter.getNotablePrice(a, b, query, inp)
            if notableData != 0:
                all_averages.append(notableData)
            break



    # section for creating Tkinter window
    root = Tk()
    root.title("Results")
    root.geometry("1200x700")
    for i in range(0, 9):
        root.columnconfigure(i, weight=1)
    root.rowconfigure(0, weight=1)

    streeview = ScrolledMultiListbox(root, scrollmode='auto')
    streeview.grid(columnspan=9, row=0, padx=5, pady=5, sticky='nsew')
    streeview.grab_current()
    treeview = streeview.listbox


    treeview.focus_set()
    treeview.config(columns=('Name', 'Listings', 'Tries', 'Craft', 'First',
                            'AVG price', 'Profit', 'PPT', 'LPPT', 'ilvl', 'Category'), command=open_link)

    for item in all_averages:
        treeview.insert(END, item['name'], item['listings'], item['tries'], item['craft'], item['first'],
                        item['average'], item['profit'], item['PPT'], item['LPPT'], item['ilvl'], item['category'])


    result_time = round(time.time() - start_time, 3)
    Label(root, text="Executed in " + str(result_time) + " seconds").grid(column=0)

    # sadly i didn't find a way to execute a function when pressing the column name, so I have to resort to manual sorting with buttons
    Button(root, text="Sort by listings", command=lambda: sort_items(
        "listings")).grid(column=1, row=1)
    Button(root, text="Sort by tries", command=lambda: sort_items(
        "tries")).grid(column=2, row=1)
    Button(root, text="Sort by price", command=lambda: sort_items(
        "average")).grid(column=3, row=1)
    Button(root, text="Sort by profit", command=lambda: sort_items(
        "profit")).grid(column=4, row=1)
    Button(root, text="Sort by PPT", command=lambda: sort_items(
        "PPT")).grid(column=5, row=1)
    Button(root, text="Sort by LPPT", command=lambda: sort_items(
        "LPPT")).grid(column=6, row=1)
    Button(root, text="Refresh", command=lambda: update()).grid(column=7, row=1)

    toggle_console(0)

    root.mainloop()
except:
    print(sys.exc_info())
    stop = int(input())