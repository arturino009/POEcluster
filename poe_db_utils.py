import requests
from bs4 import BeautifulSoup
import trade_api_utils
import json
import os
from itertools import combinations

headers = requests.utils.default_headers()

headers.update({
    'User-Agent': "IDareYouLV's cluster notable combination price checker",
    'From': 'arturino009@gmail.com'
})

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def get_data_poedb(size):
    listOfClusters = list()
    link = "https://poedb.tw/us/" + size + "_Cluster_Jewel#EnchantmentModifiers"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find(id="EnchantmentModifiers")
    listOfClustersData = table.findAll('button')
    for cluster in listOfClustersData:
        listOfNotables = list()
        weightOfNotables = 0
        clusterId = ''
        parent = cluster.find_parent('td')
        nameOfCluster = parent.contents[0].text
        nameOfCluster = nameOfCluster.split("(", 1)[0]
        if nameOfCluster == "3% increased effect of Non-Curse Auras from your Skills" or nameOfCluster == "2% increased Effect of your Curses":
            continue
        elif nameOfCluster == "12% increased Trap Damage12% increased Mine Damage":
            nameOfCluster = "12% increased Trap Damage\n12% increased Mine Damage"
        elif nameOfCluster == "10% increased Life Recovery from Flasks10% increased Mana Recovery from Flasks":
            nameOfCluster = "10% increased Life Recovery from Flasks\n10% increased Mana Recovery from Flasks"
        actualData = parent.contents[4]
        listOfNotablesData = actualData.find('tbody').contents
        for notable in listOfNotablesData:
            try:
                notableName = notable.contents[0].contents[1].text
                if "Added Small Passive Skills also grant:" in notableName:
                    continue
                notableLevel = int(notable.contents[2].text)
                notableWeight = notable.contents[1].text
                weightOfNotables = weightOfNotables + int(notableWeight)
                for entry in allStats['result'][1]['entries']:
                    if ("1 Added Passive Skill is " + notableName) == entry['text']:
                        notableId = entry['id']
                        break
                notableInfo = {
                    'notableId': notableId,
                    'notableName': notableName,
                    'notableWeight': int(notableWeight),
                    'notableLevel': notableLevel
                }
                listOfNotables.append(notableInfo)
            except:
                continue

        if(size == "Small"):
            weightOfNotables = weightOfNotables + 9800      #~15800
        else:
            weightOfNotables = weightOfNotables + 8000      #~14000

        enchantIndex = find(allStats['result'], "label", "Enchant")
        statIndex = find(allStats['result'][enchantIndex]['entries'], "id", "enchant.stat_3948993189")
        for i in allStats['result'][enchantIndex]['entries'][statIndex]['option']['options']:
            if i['text'] == nameOfCluster:
                clusterId = i['id']
                break
        notableLevelBreakpoint = {}
        for notable in listOfNotables:
            if notable["notableLevel"] not in notableLevelBreakpoint:
                notableLevelBreakpoint[notable["notableLevel"]] = 0
            notableLevelBreakpoint[notable["notableLevel"]] = notableLevelBreakpoint[notable["notableLevel"]] + notable["notableWeight"]
        if clusterId == '':
            continue
        notableCount = len(listOfNotables)
        combCount = len(list(combinations(listOfNotables, 2)))
        clusterInfo = {
            'clusterId': clusterId,
            'clusterName': nameOfCluster,
            'clusterWeightPrefix': weightOfNotables,
            'clusterNotables': listOfNotables,
            'clusterNotableCount': notableCount,
            'clusterNotableCombinationCount': combCount,
            'clusterNotableLevels': dict(sorted(notableLevelBreakpoint.items()))
        }
        listOfClusters.append(clusterInfo)
    return listOfClusters


def updateClusterData():
    responseStats = requests.get(
        "https://www.pathofexile.com/api/trade/data/stats", headers=headers)
    global allStats
    allStats = responseStats.json()

    leagues = requests.get('http://api.pathofexile.com/leagues', headers=headers)
    leagues = leagues.json()
    current_league = leagues[trade_api_utils.current_league_id]['id']  # current challenge league
    file_dir = "data/" + current_league
    if (os.path.exists("data") == False):
        os.mkdir("data")
    if (os.path.exists(file_dir) == False):
        os.mkdir(file_dir)

    with open(file_dir + '/small.json', 'w') as outfile:
        json.dump(get_data_poedb("Small"), outfile)

    with open(file_dir + '/medium.json', 'w') as outfile:
        json.dump(get_data_poedb("Medium"), outfile)
    del allStats
