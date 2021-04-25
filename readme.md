# PoeCluster

PoeCluster is a tool to index all the different combinations of cluster jewels and see if it is profitable to craft them yourself.

# WARNING

Tool only indexes the notables/combinations which have more than 10 active listings at the current moment on pathofexile.com/trade.
Listing all the combinations of notables for medium cluster jewels can take up to ~15 minutes~ 3.5 HOURS because of the sheer amount of combinations (about 1200 for medium clusters). The limiting factor here is the sites' rate-limiter.
Currently the tool is allowed to make 1 request every 10 seconds, and there is nothing I can do.

# Features

* Select the categories you want to index
* Fancy user inteface with all the cluster jewels
* Index all the single notables for medium and small cluster jewels
* Index all the possible combinations of notables for medium cluster jewels
* Double click the selected jewel to open it in pathofexile.com/trade
* ~~Refresh the info about the selected notable~~
* Up to date prices for crafting the jewel
* Profit calculations
* Sorting

# Result

![example](example.png "Results")

Columns are:

* Name: name of the notable / combination of notables
* Listings: Current number of listings on pathofexile.com/trade
* Tries: How many alteration orbs are needed to hit the notable (not guaranteed, just to hit the % of notable)
* Craft: Price of crafting the item. Based on current currency prices. Does not include the price of base cluster jewel (without the rolls).
* First: Average price of the first 2 listings
* AVG price: Average median price of the first 10 listings
* Profit: Profit of crafting the notable. Formula goes: (Profit = AVG price - Craft - Price of the base cluster)
* PPT: ProfitPerTry. Just Profit divided by Tries. It's the theoretical profit you gain on each usage of alteration orb if you factor the average median of first 10 listings
* LPPT: LegitProfitPerTry. Here it calculates the Profit based on First instead of AVG price. It's the theoretical profit you gain on each usage of alteration orb if you factor in the prices of first 2 listings
* Category: Name of the jewel enchant

### Dependencies

PoeCluster uses a number of python libraries to work properly:

* requests - sending POST and GET requests to webpages OK
* statistics - for more calculations and stats
* bs4 - parse html and find necessary items
* lxml - for optimizing web-crawler
* webbrowser - open links
* PyQt5 - UI

### Installation

PoeCluster requires python to run. Tested  version 3.9.

Install the dependencies and run PoeCluster.py.

Dependencies are installed like this:

```
pip install requests
pip install bs4
pip install PyQt5
pip install lxml
```

~~Installing TkTreectrl:~~

~~You will need 2 additional files: <https://sourceforge.net/projects/tktreectrl/> and <https://sourceforge.net/projects/tkintertreectrl/>~~

~~Download this file: <https://sourceforge.net/projects/tkintertreectrl/>~~

~~Extract it somewhere.~~

~~Open terminal in extracted location and run "python setup.py install".~~

~~Navigate to C:\Users\\{yourUser}\AppData\Local\Programs\Python\Python39\tcl.~~

~~Insert here the folder treectrl2.4.1 from <https://sourceforge.net/projects/tktreectrl/>~~

### Todos

* ~~Refactor code. It's all in one file and could be a lot more readable.~~

* ~~Add auto update for data files. Currently I have to manually download all cluster pages from craftofexile.com every league / every update to cluster jewels. Also automatically download the stats.json file every new league from <https://www.pathofexile.com/api/trade/data/stats>. Also auto update current league.~~
* ~~Change crafting process from mod % to actual mod weights. It will be more accurate, and I could just get all info from poedb.tw instead of craftofexile.com.~~
* ~~Replace TktreeCtrl. It was kinda difficult to install and I couldn't figure out how to sort rows by pressing the collumn header (that's why I have buttons and I just have a different list for each button)~~.
* ~~Figure out the exact way craftofexile.com calculates augmentation orb count when crafting double prefix cluster jewels with alt+aug+regal. Other currencies I figured out correctly as far as I can tell.~~
* ~~Remove all data pages completely. Currently it parses all the downloaded pages for cluster jewels at the start of each run and it isn't efficient. I just need to add all the necessary info about cluster jewels into one/multiple files and read from there. Probably implement together with auto-update, so it just updates this file instead of downloading all the fully-JS-rendered webpages about cluster jewels every new league.~~
* Improve speed of execution? Probably impossible, because pathofexile.com/trade rate-limit already is the limiting factor.
* ~~Add ILVL's of notables/clusters in the calculations. That's a lot of work, but the calculations might be more accurate.~~ Also maybe add the calculations of prices for jewels with different number of passives.
* Add calculations for just the notable without the category. Some notables share categories, and people sometimes don't care about the base enchant of the cluster.
* ~~Create an .exe file so all the dependencies would be included? I don't know if that's really possible~~
