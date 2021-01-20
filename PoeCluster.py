from updateClusterData import updateClusterData
import priceGetter
import requests
import time
from itertools import combinations
# import webbrowser
import os
import json
import ctypes
import pandas as pd
import pandasgui as pg

def toggle_console(a):
    # hiding the console
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW_HIDE = a
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, SW_HIDE)


# def open_link(q): #deprecated for now
#     webbrowser.open('https://www.pathofexile.com/trade/search/' +
#                     priceGetter.current_league + '/' + all_averages[q]['id'])


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

    levelBreakpoints = [1,50,68,75]

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

    df = pd.DataFrame(all_averages)
    df.drop(['request', 'category_full','notable_full','id'], axis=1, inplace=True)
    #gui
    pg.show(df)
except Exception as e:
    print(e)
    stop = int(input())