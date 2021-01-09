import requests
from bs4 import BeautifulSoup
import json
import os


def get_data_poedb(size):
    listOfClusters = list()
    link = "https://poedb.tw/us/" + size + "_Cluster_Jewel"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find(
        id="DeliriumPassiveTreeExpansionSkillsn" + size + "ClusterJewel")
    listOfClustersData = table.findAll('button')
    for cluster in listOfClustersData:
        listOfNotables = list()
        weightOfNotables = 0
        parent = cluster.find_parent('td')
        nameOfCluster = parent.contents[0].text
        actualData = parent.contents[4]
        listOfNotablesData = actualData.find('tbody').contents
        for notable in listOfNotablesData:
            try:
                notableName = notable.contents[0].contents[1].text
                notableLevel = int(notable.contents[2].text)
                notableWeight = notable.contents[1].text
                weightOfNotables = weightOfNotables + int(notableWeight)
                for entry in allStats['result'][1]['entries']:
                    if notableName in entry['text']:
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
            weightOfNotables = weightOfNotables + 9800
        else:
            weightOfNotables = weightOfNotables + 8000

        for i in allStats['result'][4]['entries'][1]['option']['options']:
            if i['text'] == nameOfCluster:
                clusterId = i['id']
                break
        clusterInfo = {
            'clusterId': clusterId,
            'clusterName': nameOfCluster,
            'clusterWeightPrefix': weightOfNotables,
            'clusterNotables': listOfNotables
        }
        listOfClusters.append(clusterInfo)
    return listOfClusters


def updateClusterData():
    responseStats = requests.get(
        "https://www.pathofexile.com/api/trade/data/stats")
    global allStats
    allStats = responseStats.json()

    leagues = requests.get('http://api.pathofexile.com/leagues')
    leagues = leagues.json()
    current_league = leagues[4]['id']  # current challenge league
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
