
import requests                     #so I can send POST and GET requests to webpages
import time                         #so I can make a time delay
from itertools import combinations  #so I get all possible combinations of elements in a list
import statistics                   #so i get averages and medians of lists
from tkinter import *               #so I can make fancy interface
from TkTreectrl import *            #so I can make even fancier multiListBoxes  (manual installation required)
import webbrowser                   #so i can open links in browser
import list_categories              #other file with a lot of manually written code

#start the timer for program execution
start_time = time.time()
   
#import all lists from list_categories.py file
lists = list_categories.make_lists()

#wasting_aff = 'explicit.stat_2066820199'
#vivid_hues = 'explicit.stat_3957006524'
current_exa_price = 137                                             #current exa price https://poe.ninja/challenge/currency/exalted-orb


#list of all values that I will get
all_averages = list()

#clear the files
open('output.txt', 'w').close()
open('expensive.txt', 'w').close()

for a in lists:
    #make a list of all possible combinations of items in each category
    comb = list(combinations(a['list'],2))
    for b in comb:
        data_set = {        #structure for API request. All info from https://www.reddit.com/r/pathofexiledev/comments/7aiil7/how_to_make_your_own_queries_against_the_official/ . Absolutely no other documentation
            "query": {
                "status": {
                    "option": "online"
                },
                "type": "Medium Cluster Jewel",
                "stats": [{
                    "type": "and",
                                   #value1                 #value2                  #category
                    "filters": [{"id":b[0]['id']['id']}, {"id":b[1]['id']['id']}, {"id":'enchant.stat_3948993189',
                                                                                   "value":{"option":a['id']}
                                                                                   }]
                }],
                "filters": {
                    "type_filters": {
                        "filters": {
                            "rarity": {
						        "option": "rare"
					            }
                            }
                        }
                    }
            },
            "sort": {
                "price": "asc"
            }
        }
        #time delay, so API wont rate limit me
        time.sleep(0.4)
        
        #send the request to API
        response = requests.post('https://www.pathofexile.com/api/trade/search/Harvest', json=data_set)
        response = response.json()
        result = response['result']
        id = response['id']
        size = response['total']

        #if there are less than 10 listings for an item, we just just skip it (no demand)
        if size < 10:
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
        address = 'https://www.pathofexile.com/api/trade/fetch/' + str(str1) + '?query=' + id
        request = requests.get(address)
        results_json = request.json()
        
        #probability to get an item while crafting. Formula is mostly correct
        probability = b[0]['percent'] * b[1]['percent'] / 19.2
        #get number of tries to get item
        tries = 100 / probability   

        #approximate cost of 1 try
        cost_of_try = 0.36

        #price to create an item (approximate)
        price = tries * cost_of_try

        #list to hold all prices of an item. Later used to calculate medium price
        medium = list()

        f = open("output.txt", "a")
        expensive = open("expensive.txt", "a")

        f.write(b[0]['id']['text'] + " and " + b[1]['id']['text'] + ": " + str(round(probability,3)) + "%" + " Cost for rerolls: " + str(round(price,2)) + " Tries: " + str(round(tries)) + '\n')
        f.write('Listings:' + str(size) + '\n')
        print(b[0]['id']['text'] + " and " + b[1]['id']['text'] + ": " +  str(round(probability,3))  + "%" + " Cost for rerolls: " + str(round(price,2))+ " Tries: " + str(round(tries)))
        print('Listings:' + str(size))
        
        #used to calculate actual count of items with prices
        count = 0
        for p in results_json['result']:
            #if item has no price listed, set as No price
            if(p['listing']['price'] != None):
                count = count + 1   
                #conversion for some more valuable currency
                if(p['listing']['price']['currency'] == "exalted"):
                    p['listing']['price']['amount'] = p['listing']['price']['amount'] * current_exa_price
                    p['listing']['price']['currency'] = "chaos"
                if(p['listing']['price']['currency'] == "chaos"):
                    medium.append(p['listing']['price']['amount'])
                print("Price: ", p['listing']['price']['amount'], " " , p['listing']['price']['currency'], '\n')
                f.write("Price: " + str(p['listing']['price']['amount']) + " " + p['listing']['price']['currency'] + '\n')
            else:
                print("No price")   
        #get the average median of all listed prices for an item
        avg = statistics.median_grouped(medium)
        #profit margin 
        profit = avg - price
        print("The average median is ", round(avg,2), "     Profit:", round(profit,2), '\n')
        f.write("The average median is                             " + str(round(avg,2)) + " Profit:          " + str(round(profit,2)) + '\n')
        #if less than 10 listings have prices, skip the item
        if count == 10:
            x = {
                'name': b[0]['id']['text'] + " and " + b[1]['id']['text'],
                'listings': size,
                'tries': round(tries),
                'average': round(avg,2),
                'profit': round(profit,2),
                'PPT': round(profit/tries,3),
                'category': a['category'],
                'id': id
                }
            all_averages.append(x)
            #if there is profit to be made, print to different file
            if x['profit'] > 0:
                expensive.write(str(x) + '\n')
                expensive.write('Profit per try:'+ str(round(profit/tries,3)) + '\n')
        medium.clear()
        f.close()
        expensive.close()    


#lists made for sorting
sorted_list_count = list()
sorted_list_tries = list()
sorted_list_price = list()
sorted_list_profit = list()
sorted_list_ppt = list()

sorted_list_count = sorted(all_averages, key = lambda i: i['listings'],reverse=True)
sorted_list_tries = sorted(all_averages, key = lambda i: i['tries'],reverse=True)
sorted_list_price = sorted(all_averages, key = lambda i: i['average'],reverse=True)
sorted_list_profit = sorted(all_averages, key = lambda i: i['profit'],reverse=True)
sorted_list_ppt = sorted(all_averages, key = lambda i: i['PPT'],reverse=True)


#need to keep track of currently displayed list
current_sort = list()
current_sort = all_averages

def open_link(q):
    webbrowser.open('https://www.pathofexile.com/trade/search/Harvest/' + current_sort[q]['id'])


#section for creating Tkinter window
root = Tk()
root.title("Results")
root.geometry("1200x800")
for i in range(0, 6):
     root.columnconfigure(i, weight=1)
root.rowconfigure(0, weight=1)

streeview = ScrolledMultiListbox(root, scrollmode = 'auto')
streeview.grid(columnspan=6, row=0, padx=5,pady=5,sticky='nsew')
treeview = streeview.listbox
treeview.focus_set()
treeview.config(columns=('Name', 'Listings','Tries','Average price','Profit','PPT', 'Category'), command=open_link)
for item in all_averages:
    treeview.insert(END,item['name'],item['listings'],item['tries'],item['average'],item['profit'],item['PPT'], item['category'])

#replacing the listbox with requested sort
def sort_items(given_list):
    treeview.delete(ALL)
    global current_sort
    current_sort = given_list
    for item in given_list:
        treeview.insert(END,item['name'],item['listings'],item['tries'],item['average'],item['profit'],item['PPT'], item['category'])

result_time = round(time.time() - start_time, 3)
time_label = Label(root, text="Executed in " + str(result_time) + " seconds").grid(column=0)

#sadly i didn't find a way to execute a function when pressing the column name, so I have to resort to manual sorting with buttons
button2 = Button(root,text="Sort by listings", command=lambda:sort_items(sorted_list_count)).grid(column=1, row=1)
button3 = Button(root,text="Sort by tries", command=lambda:sort_items(sorted_list_tries)).grid(column=2, row=1)
button4 = Button(root,text="Sort by price", command=lambda:sort_items(sorted_list_price)).grid(column=3, row=1)
button5 = Button(root,text="Sort by profit", command=lambda:sort_items(sorted_list_profit)).grid(column=4, row=1)
button6 = Button(root,text="Sort by PPT", command=lambda:sort_items(sorted_list_ppt)).grid(column=5, row=1)


root.mainloop()