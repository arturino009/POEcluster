
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
                for i in data['result'][4]['entries'][0]['option']['options']:
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

session = HTMLSession()
resp = session.get("https://poe.ninja/challenge/currency/exalted-orb")
resp.html.render()
soup = BeautifulSoup(resp.html.html, "lxml")
res = soup.find_all("span", class_="currency-amount")
current_exa_price = round(float(res[0].contents[0]))                                             #current exa price https://poe.ninja/challenge/currency/exalted-orb

#list of all values that I will get
all_averages = list()
all_averages.clear()
for a in all_lists:
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
                        }
                    }
            },
            "sort": {
                "price": "asc"
            }
        }
        #send the request to API
        print("Sending request...")
        response = requests.post('https://www.pathofexile.com/api/trade/search/Harvest', json=data_set)
        response = response.json()
        print("Got response!")

        result = response['result']
        id = response['id']
        size = response['total']

        #if there are less than 10 listings for an item, we just just skip it (no demand)
        if size < 5:
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

        #time delay, so API wont rate limit me
        time.sleep(0.4)
        #get all actual listings of items
        print("Requesting item info...")
        address = 'https://www.pathofexile.com/api/trade/fetch/' + str(str1) + '?query=' + id
        request = requests.get(address)
        results_json = request.json()
        
        #probability to get an item while crafting. Formula is mostly correct
        if query == 1:
            probability = b['prefix']
            cost_of_try = 0.05
        else:
            probability = b[0]['weight'] * b[1]['weight'] / 19.2
            cost_of_try = 0.36

        #get number of tries to get item
        tries = 100 / probability   

        #price to create an item (approximate)
        price = tries * cost_of_try

        #list to hold all prices of an item. Later used to calculate medium price
        medium = list()

        if query == 1:
            print(b['name'] + ": " +  str(round(probability,3))  + "%" + " Cost for rerolls: " + str(round(price,2))+ " Tries: " + str(round(tries)))
            print('Listings:' + str(size))
        else:
            print(b[0]['name'] + " and " + b[1]['name'] + ": " +  str(round(probability,3))  + "%" + " Cost for rerolls: " + str(round(price,2))+ " Tries: " + str(round(tries)))
            print('Listings:' + str(size))
        
        #used to calculate actual count of items with prices
        count = 0
        for p in results_json['result']:
            #if item has no price listed, set as No price
            if(p['listing']['price'] != None):
                #conversion for some more valuable currency
                if(p['listing']['price']['currency'] == "exalted"):
                    p['listing']['price']['amount'] = p['listing']['price']['amount'] * current_exa_price
                    p['listing']['price']['currency'] = "chaos"
                if(p['listing']['price']['currency'] == "chaos"):
                    count = count + 1 
                    medium.append(p['listing']['price']['amount'])
                print("Price: ", p['listing']['price']['amount'], " " , p['listing']['price']['currency'], '\n')
            else:
                print("No price") 
        #if less than 10 listings have prices, skip the item
        if count > 4:
            #get the average median of all listed prices for an item
            avg = statistics.median_grouped(medium)
            #profit margin 
            profit = avg - price - 1
            first = (medium[0]+medium[1])/2
            LPPT = (first - price - 1)/tries
            print("The average median is ", round(avg,2), "     Profit:", round(profit,2), '\n')
            x = {
                'name': b['name'] if query == 1 else (b[0]['name'] + " and " + b[1]['name']),
                'listings': size,
                'tries': round(tries),
                'first': round(first,2),
                'average': round(avg,2),
                'profit': round(profit,2),
                'PPT': round(profit/tries,3),
                'LPPT': round(LPPT,3),    #when first item is a lot cheaper than average
                'category': a['category'],
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
    webbrowser.open('https://www.pathofexile.com/trade/search/Harvest/' + current_sort[q]['id'])

#section for creating Tkinter window
root = Tk()
root.title("Results")
root.geometry("1200x800")
for i in range(0, 7):
     root.columnconfigure(i, weight=1)
root.rowconfigure(0, weight=1)

streeview = ScrolledMultiListbox(root, scrollmode = 'auto')
streeview.grid(columnspan=7, row=0, padx=5,pady=5,sticky='nsew')
treeview = streeview.listbox
treeview.focus_set()
treeview.config(columns=('Name', 'Listings','Tries','First','AVG price','Profit','PPT', 'LPPT', 'Category'), command=open_link)
for item in all_averages:
    treeview.insert(END,item['name'],item['listings'],item['tries'],item['first'],item['average'],item['profit'],item['PPT'], item['LPPT'], item['category'])

#replacing the listbox with requested sort
def sort_items(given_list):
    treeview.delete(ALL)
    global current_sort
    current_sort = given_list
    for item in given_list:
        treeview.insert(END,item['name'],item['listings'],item['tries'],item['first'],item['average'],item['profit'],item['PPT'], item['LPPT'], item['category'])

result_time = round(time.time() - start_time, 3)
time_label = Label(root, text="Executed in " + str(result_time) + " seconds").grid(column=0)

#sadly i didn't find a way to execute a function when pressing the column name, so I have to resort to manual sorting with buttons
button2 = Button(root,text="Sort by listings", command=lambda:sort_items(sorted_list_count)).grid(column=1, row=1)
button3 = Button(root,text="Sort by tries", command=lambda:sort_items(sorted_list_tries)).grid(column=2, row=1)
button4 = Button(root,text="Sort by price", command=lambda:sort_items(sorted_list_price)).grid(column=3, row=1)
button5 = Button(root,text="Sort by profit", command=lambda:sort_items(sorted_list_profit)).grid(column=4, row=1)
button6 = Button(root,text="Sort by PPT", command=lambda:sort_items(sorted_list_ppt)).grid(column=5, row=1)
button7 = Button(root,text="Sort by LPPT", command=lambda:sort_items(sorted_list_lppt)).grid(column=6, row=1)

#hiding the console
kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
SW_HIDE = 0
hWnd = kernel32.GetConsoleWindow()
if hWnd:
    user32.ShowWindow(hWnd, SW_HIDE)

root.mainloop()