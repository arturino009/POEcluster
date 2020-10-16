import requests                     #so I can send POST and GET requests to webpages
import time                         #so I can make a time delay
from itertools import combinations  #so I get all possible combinations of elements in a list
import statistics                   #so i get averages and medians of lists
from tkinter import *               #so I can make fancy interface
from TkTreectrl import *            #so I can make even fancier multiListBoxes  (manual installation required)
import webbrowser                   #so i can open links in browser
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import os
import json
import ctypes
import codecs
import math

def toggle_console(a):
    #hiding the console
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW_HIDE = a
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, SW_HIDE)


print('Input 1 for single notable prices, 2 for double notable prices.') 
query = int(input())
inp = 0
if query == 1:
    print('Input 1 to check small cluster jewels, 2 for medium cluster jewels.') 
    inp = int(input())
    location = "/data/small/" if inp == 1 else "/data/medium/"
else:
    location = "/data/medium/"

all_lists = list()

for filename in os.listdir(os.getcwd() + location):
    with open(os.getcwd() + location + filename) as data_file:
        contents = data_file.read()
        soup = BeautifulSoup(contents, 'lxml')
        results = soup.findAll("div", {"modgrp" : "unique_notable"} if inp == 1 else {"modgrp" : re.compile("Notable")})
        nameofcategory = soup.findAll("div", {"class": "choice med_shadow"})
        weightofaffix = soup.findAll("div", {"class": "tpct"})
        a = list() 
        for g in results:
            with open('stats.json') as json_file:
                data = json.load(json_file)
                for i in data['result'][1]['entries']:
                    if i['text'] == g.contents[0].text:
                        b = {
                            'id': i['id'],
                            'name': g.contents[0].text,
                            'prefix': float(g.contents[4].text[:-1]),
                            'weight': float(g.contents[5].text[:-1])
                            }
                        a.append(b)
                        print(g.contents[0].text)
                        continue
        if "@" in filename:
            filename = filename.replace("@", '\\')[:-5]
        else:
            filename = filename[:-5]
        with open('stats.json') as json_file:
                data = json.load(json_file)
                for i in data['result'][4]['entries'][1]['option']['options']:
                    if i['text'] == codecs.decode(filename, 'unicode_escape'):
                        id = i['id']
                        break
        c = {
            'id': id,
            'category': filename,
            'notables': a
            }
        all_lists.append(c)


#start the timer for program execution
start_time = time.time()

acceptable_listings = 10
try:
    session = HTMLSession()
    resp = session.get("https://poe.ninja/challenge/currency/exalted-orb")
    resp.html.render(sleep=2)
    soup = BeautifulSoup(resp.html.html, "lxml")
    res = soup.find_all("span", class_="currency-amount")
    current_exa_price = round(float(res[0].contents[0]))                                             #current exa price https://poe.ninja/challenge/currency/exalted-orb
    print("Exalt price: " + str(current_exa_price))
except:
    current_exa_price = 62
    print("Couldn't get exalt info from poe.ninja. Using default value: " + str(current_exa_price))

try:
    session = HTMLSession()
    resp = session.get("https://poe.ninja/challenge/currency/orb-of-alchemy")
    resp.html.render(sleep=2)
    soup = BeautifulSoup(resp.html.html, "lxml")
    res = soup.find_all("span", class_="currency-amount")
    current_alch_price = round(1/float(res[1].contents[0]),3)
    print("Alch price: " + str(current_alch_price))
except:
    current_alch_price = 0.20
    print("Couldn't get alch info from poe.ninja. Using default value: " + str(current_alch_price))

try:
    session = HTMLSession()
    resp = session.get("https://poe.ninja/challenge/currency/orb-of-alteration")
    resp.html.render(sleep=2)
    soup = BeautifulSoup(resp.html.html, "lxml")
    res = soup.find_all("span", class_="currency-amount")
    current_alt_price = round(1/float(res[1].contents[0]),3)
    print("Alt price: " + str(current_alt_price))
except:
    current_alt_price = 0.21
    print("Couldn't get alt info from poe.ninja. Using default value: " + str(current_alt_price))

try:
    session = HTMLSession()
    resp = session.get("https://poe.ninja/challenge/currency/orb-of-augmentation")
    resp.html.render(sleep=2)
    soup = BeautifulSoup(resp.html.html, "lxml")
    res = soup.find_all("span", class_="currency-amount")
    current_aug_price = round(1/float(res[1].contents[0]),3)
    print("Aug price: " + str(current_aug_price))
except:
    current_aug_price = 0.08
    print("Couldn't get aug info from poe.ninja. Using default value: " + str(current_aug_price))

# try:
#     session = HTMLSession()
#     resp = session.get("https://poe.ninja/challenge/currency/regal-orb")
#     resp.html.render(sleep=2)
#     soup = BeautifulSoup(resp.html.html, "lxml")
#     res = soup.find_all("span", class_="currency-amount")
#     current_regal_price = round(1/float(res[1].contents[0]),3)
#     print("Regal price: " + str(current_regal_price))
# except:
#     current_regal_price = 0.13
#     print("Couldn't get regal info from poe.ninja. Using default value: " + str(current_regal_price))

# try:
#     session = HTMLSession()
#     resp = session.get("https://poe.ninja/challenge/currency/orb-of-scouring")
#     resp.html.render(sleep=2)
#     soup = BeautifulSoup(resp.html.html, "lxml")
#     res = soup.find_all("span", class_="currency-amount")
#     current_scour_price = round(1/float(res[1].contents[0]),3)
#     print("Scour price: " + str(current_scour_price))
# except:
#     current_scour_price = 0.43
#     print("Couldn't get scour info from poe.ninja. Using default value: " + str(current_scour_price))

# try:
#     session = HTMLSession()
#     resp = session.get("https://poe.ninja/challenge/currency/orb-of-transmutation")
#     resp.html.render(sleep=2)
#     soup = BeautifulSoup(resp.html.html, "lxml")
#     res = soup.find_all("span", class_="currency-amount")
#     current_trans_price = round(1/float(res[1].contents[0]),3)
#     print("Trans price: " + str(current_trans_price))
# except:
#     current_trans_price = 0.04
#     print("Couldn't get trans info from poe.ninja. Using default value: " + str(current_trans_price))


def get_category_jewel_price(a):
    data_set = {        #structure for API request. All info from https://www.reddit.com/r/pathofexiledev/comments/7aiil7/how_to_make_your_own_queries_against_the_official/ . Absolutely no other documentation
        "query": {
            "status": {
                "option": "online"
            },
            "stats": [{
                "type": "and",
                "filters": [{"id":'enchant.stat_3948993189', "value":{"option":a['id']}}]
            }],
            "filters": {
                "type_filters": {
                    "filters": {
                        "rarity": {
						    "option": "nonunique"
					        }
                        }
                    },
                "misc_filters":{
                    "filters":{
                        "corrupted":{
                            "option": "false"
                            }
                        }
                    },
                "trade_filters": {
                        "filters":{
                            "sale_type":{
                                "option": "priced"
                                }
                            }
                        }
                }
        },
        "sort": {
            "price": "asc"
        }
    }
    #send the request to API
    print("Sending request...")
    try:
        response = requests.post('https://www.pathofexile.com/api/trade/search/Heist', json=data_set)
        response = response.json()
        print("Got response!")
    except Exception as e:
        print(e)
        print("Waiting 60 seconds.") 
        time.sleep(60)
    result = response['result']
    id = response['id']
    size = response['total']

    #if there are more than 10 listings, strip all of them away after 10th. We cant request info about items more than 10 items at once
    if size > 10:
        del result[10:]

    #make correct formatting
    if size > 1:
        str1 = ','.join(result)
    else:
        str1 = result

    #time delay, so API wont rate limit me
    time.sleep(0.4)
    #get all actual listings of items
    print("Requesting item info...")
    address = 'https://www.pathofexile.com/api/trade/fetch/' + str(str1) + '?query=' + id
    request = requests.get(address)
    results_json = request.json()
    #list to hold all prices of an item. Later used to calculate medium price
    medium = list()
    print(a['category'])
    print('Listings:' + str(size))
    for p in results_json['result']:
        #conversion for some more valuable currency
        if(p['listing']['price']['currency'] == "exalted"):
            p['listing']['price']['amount'] = p['listing']['price']['amount'] * current_exa_price
            p['listing']['price']['currency'] = "chaos"
        elif(p['listing']['price']['currency'] == "alch"):
            p['listing']['price']['amount'] = p['listing']['price']['amount'] * current_alch_price
            p['listing']['price']['currency'] = "chaos"
        if(p['listing']['price']['currency'] == "chaos"):
            medium.append(p['listing']['price']['amount'])
        print("Price: ", p['listing']['price']['amount'], " " , p['listing']['price']['currency'], '\n')
    #get the average median of all listed prices for an item
    avg =  statistics.median_grouped(medium)
    print("The average median is " + str(round(avg,2)) + '\n')
    return avg

#list of all values that I will get
all_averages = list()
all_averages.clear()
for a in all_lists:
    jewel_price = get_category_jewel_price(a)
    if query == 1:
        comb = a['notables']
    else:
        #make a list of all possible combinations of items in each category
        comb = list(combinations(a['notables'],2))
    for b in comb:
        data_set = {        #structure for API request. All info from https://www.reddit.com/r/pathofexiledev/comments/7aiil7/how_to_make_your_own_queries_against_the_official/ . Absolutely no other documentation
            "query": {
                "status": {
                    "option": "online"
                },
                "type": "Small Cluster Jewel" if inp == 1 else "Medium Cluster Jewel",
                "stats": [{
                    "type": "and",
                                    #value1                   #category
                    #"filters": [{"id":'enchant.stat_3948993189', "value":{"option":a['id']}}, {"id":b['id']}] if query == 1 else [{"id":'enchant.stat_3948993189', "value":{"option":a['id']}}, {"id":b[0]['id']}, {"id":b[1]['id']}]
                    "filters": [{"id":b['id']}] if query == 1 else [{"id":b[0]['id']}, {"id":b[1]['id']}]
                }],
                "filters": {
                    "type_filters": {
                        "filters": {
                            "rarity": {
						        "option": "nonunique"
					            }
                            }
                        },
                    "trade_filters": {
                        "filters":{
                            "sale_type":{
                                "option": "priced"
                                }
                            }
                        }
                    }
            },
            "sort": {
                "price": "asc"
            }
        }
        #time delay, so API won't rate limit me
        time.sleep(0.4)
        #send the request to API
        print("Sending request...")
        try:
            response = requests.post('https://www.pathofexile.com/api/trade/search/Heist', json=data_set)
            response = response.json()
            print("Got response!")
        except Exception as e:
            print(e)
            print("Waiting 60 seconds.") 
            time.sleep(60)

        result = response['result']
        id = response['id']
        size = response['total']

        #if there are less than 10 listings for an item, we just just skip it (no demand)
        if size < acceptable_listings:
            print("Not enough items! Skipping...")
            continue    

        #if there are more than 10 listings, strip all of them away after 10th. We cant request info about items more than 10 items at once
        if size > 10:
            del result[10:]

        #make correct formatting
        if size > 1:
            str1 = ','.join(result)
        else:
            str1 = result

        #get all actual listings of items
        print("Requesting item info...")
        address = 'https://www.pathofexile.com/api/trade/fetch/' + str(str1) + '?query=' + id
        request = requests.get(address)
        results_json = request.json()
        
        #probability to get an item while crafting. Formula is mostly correct
        if query == 1:
            probability = b['prefix']
            cost_of_try = 0.25 * current_aug_price + current_alt_price
        else:
            probability = (b[0]['weight'] * b[1]['prefix'] + b[1]['weight'] * b[0]['prefix'])/100
            cost_of_try = 0.3

        #get number of tries to get item
        tries = math.ceil(100 / probability)

        #price to create an item (approximate)
        craft_price = tries * cost_of_try

        craft_and_jewel_price = craft_price + jewel_price

        #list to hold all prices of an item. Later used to calculate medium price
        medium = list()

        if query == 1:
            print(b['name'] + ": " +  str(round(probability,3))  + "%" + " Cost for rerolls: " + str(round(craft_price,2))+ " Tries: " + str(round(tries)))
            print('Listings:' + str(size))
        else:
            print(b[0]['name'] + " and " + b[1]['name'] + ": " +  str(round(probability,3))  + "%" + " Cost for rerolls: " + str(round(craft_price,2))+ " Tries: " + str(round(tries)))
            print('Listings:' + str(size))
        
        for p in results_json['result']:
            #conversion for some more valuable currency
            if(p['listing']['price']['currency'] == "exalted"):
                p['listing']['price']['amount'] = p['listing']['price']['amount'] * current_exa_price
                p['listing']['price']['currency'] = "chaos"
            elif(p['listing']['price']['currency'] == "alch"):
                p['listing']['price']['amount'] = p['listing']['price']['amount'] * current_alch_price
                p['listing']['price']['currency'] = "chaos"
            if(p['listing']['price']['currency'] == "chaos"):
                medium.append(p['listing']['price']['amount'])
            print("Price: ", p['listing']['price']['amount'], " " , p['listing']['price']['currency'], '\n')

        #get the average median of all listed prices for an item
        avg = statistics.median_grouped(medium)
        #profit margin 
        profit = avg - craft_and_jewel_price
        PPT = profit/tries
        first = (medium[0]+medium[1])/2
        LPPT = (first - craft_and_jewel_price)/tries
        print("The average median is ", round(avg,2), "     Profit:", round(profit,2), '\n')
        x = {
            'name': b['name'] if query == 1 else (b[0]['name'] + " and " + b[1]['name']),
            'listings': size,
            'tries': round(tries),
            'craft': round(craft_and_jewel_price, 2),
            'first': round(first,2),
            'average': round(avg,2),
            'profit': round(profit,2),
            'PPT': round(PPT,3),
            'LPPT': round(LPPT,3),    #when first item is a lot cheaper than average
            'category': a['category'],
            'request': data_set,
            'category_full': a,
            'id': id
            }
        all_averages.append(x)
        medium.clear()

#lists made for sorting
sorted_list_count = list()
sorted_list_tries = list()
sorted_list_price = list()
sorted_list_profit = list()
sorted_list_ppt = list()
sorted_list_lppt = list()

sorted_list_count = sorted(all_averages, key = lambda i: i['listings'],reverse=True)
sorted_list_tries = sorted(all_averages, key = lambda i: i['tries'],reverse=True)
sorted_list_price = sorted(all_averages, key = lambda i: i['average'],reverse=True)
sorted_list_profit = sorted(all_averages, key = lambda i: i['profit'],reverse=True)
sorted_list_ppt = sorted(all_averages, key = lambda i: i['PPT'],reverse=True)
sorted_list_lppt = sorted(all_averages, key = lambda i: i['LPPT'],reverse=True)
#need to keep track of currently displayed list

current_sort = list()
current_sort = all_averages

def open_link(q):
    webbrowser.open('https://www.pathofexile.com/trade/search/Heist/' + current_sort[q]['id'])

#replacing the listbox with requested sort
def sort_items(given_list):
    treeview.delete(ALL)
    global current_sort
    current_sort = given_list
    for item in given_list:
        treeview.insert(END,item['name'],item['listings'],item['tries'], item['craft'],item['first'],item['average'],item['profit'],item['PPT'], item['LPPT'], item['category'])


def update():
    global current_sort
    global sorted_list_count
    global sorted_list_tries
    global sorted_list_price
    global sorted_list_profit
    global sorted_list_ppt
    global sorted_list_lppt
    toggle_console(1)
    a = treeview.curselection()[0]
    b = current_sort[a]
    jewel_price = get_category_jewel_price(b['category_full'])
    print("Sending request...")
    response = requests.post('https://www.pathofexile.com/api/trade/search/Heist', json=b['request'])
    response = response.json()
    print("Got response!")

    result = response['result']
    id = response['id']
    size = response['total']

    #if there are less than 10 listings for an item, we just just skip it (no demand)
    if size < acceptable_listings:
        print("Not enough items! Skipping...")
        current_sort.pop(a)
        return    

    #if there are more than 10 listings, strip all of them away after 10th. We cant request info about items more than 10 items at once
    if size > 10:
        del result[10:]

    #make correct formatting
    if size > 1:
        str1 = ','.join(result)
    else:
        str1 = result

    #time delay, so API wont rate limit me
    time.sleep(0.4)
    #get all actual listings of items
    print("Requesting item info...")
    address = 'https://www.pathofexile.com/api/trade/fetch/' + str(str1) + '?query=' + id
    request = requests.get(address)
    results_json = request.json()

    #price to create an item (approximate)
    craft_price = b['tries'] * cost_of_try

    craft_and_jewel_price = craft_price + jewel_price

    #list to hold all prices of an item. Later used to calculate medium price
    medium = list()

    print(b['name'] + ": " + " Cost for rerolls: " + str(round(craft_price,2))+ " Tries: " + str(round(b['tries'])))
    print('Listings:' + str(size))
        
    for p in results_json['result']:
        #conversion for some more valuable currency
        if(p['listing']['price']['currency'] == "exalted"):
            p['listing']['price']['amount'] = p['listing']['price']['amount'] * current_exa_price
            p['listing']['price']['currency'] = "chaos"
        elif(p['listing']['price']['currency'] == "alch"):
            p['listing']['price']['amount'] = p['listing']['price']['amount'] * current_alch_price
            p['listing']['price']['currency'] = "chaos"
        if(p['listing']['price']['currency'] == "chaos"):
            medium.append(p['listing']['price']['amount'])
        print("Price: ", p['listing']['price']['amount'], " " , p['listing']['price']['currency'], '\n')
    
    #get the average median of all listed prices for an item
    avg = statistics.median_grouped(medium)
    #profit margin 
    profit = avg - craft_and_jewel_price
    PPT = profit/b['tries']
    first = (medium[0]+medium[1])/2
    LPPT = (first - craft_and_jewel_price)/b['tries']
    print("The average median is ", round(avg,2), "     Profit:", round(profit,2), '\n')
    x = {
        'name': b['name'],
        'listings': size,
        'tries': b['tries'],
        'craft': round(craft_and_jewel_price, 2),
        'first': round(first,2),
        'average': round(avg,2),
        'profit': round(profit,2),
        'PPT': round(PPT,3),
        'LPPT': round(LPPT,3),    #when first item is a lot cheaper than average
        'category': b['category'],
        'request': b['request'],
        'category_full': b['category_full'],
        'id': id
        }
    current_sort[a] = x
    medium.clear()
    sorted_list_count = sorted(current_sort, key = lambda i: i['listings'],reverse=True)
    sorted_list_tries = sorted(current_sort, key = lambda i: i['tries'],reverse=True)
    sorted_list_price = sorted(current_sort, key = lambda i: i['average'],reverse=True)
    sorted_list_profit = sorted(current_sort, key = lambda i: i['profit'],reverse=True)
    sorted_list_ppt = sorted(current_sort, key = lambda i: i['PPT'],reverse=True)
    sorted_list_lppt = sorted(current_sort, key = lambda i: i['LPPT'],reverse=True)
    sort_items(current_sort)
    toggle_console(0)

#section for creating Tkinter window
root = Tk()
root.title("Results")
root.geometry("1200x700")
for i in range(0, 8):
     root.columnconfigure(i, weight=1)
root.rowconfigure(0, weight=1)

streeview = ScrolledMultiListbox(root, scrollmode = 'auto')
streeview.grid(columnspan=8, row=0, padx=5,pady=5,sticky='nsew')
streeview.grab_current()
treeview = streeview.listbox


treeview.focus_set()
treeview.config(columns=('Name', 'Listings','Tries', 'Craft','First','AVG price','Profit','PPT', 'LPPT', 'Category'), command=open_link)

for item in all_averages:
    treeview.insert(END,item['name'],item['listings'],item['tries'], item['craft'],item['first'],item['average'],item['profit'],item['PPT'], item['LPPT'], item['category'])



result_time = round(time.time() - start_time, 3)
time_label = Label(root, text="Executed in " + str(result_time) + " seconds").grid(column=0)

#sadly i didn't find a way to execute a function when pressing the column name, so I have to resort to manual sorting with buttons
button2 = Button(root,text="Sort by listings", command=lambda:sort_items(sorted_list_count)).grid(column=1, row=1)
button3 = Button(root,text="Sort by tries", command=lambda:sort_items(sorted_list_tries)).grid(column=2, row=1)
button4 = Button(root,text="Sort by price", command=lambda:sort_items(sorted_list_price)).grid(column=3, row=1)
button5 = Button(root,text="Sort by profit", command=lambda:sort_items(sorted_list_profit)).grid(column=4, row=1)
button6 = Button(root,text="Sort by PPT", command=lambda:sort_items(sorted_list_ppt)).grid(column=5, row=1)
button7 = Button(root,text="Sort by LPPT", command=lambda:sort_items(sorted_list_lppt)).grid(column=6, row=1)
button8 = Button(root,text="Refresh", command=lambda:update()).grid(column=7, row=1)

toggle_console(0)

root.mainloop()