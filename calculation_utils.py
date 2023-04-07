from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from itertools import combinations
import trade_api_utils

class NotableCombinationCalculator(QObject):
    finished = pyqtSignal()
    data_updated = pyqtSignal(object)

    def __init__(self, selected_cluster_jewels, query, inp):
        super().__init__()
        self.selected_cluster_jewels = selected_cluster_jewels
        self.query = query
        self.inp = inp

    @pyqtSlot()
    def process(self):
        # all the code that updates the data goes here
        all_averages = list()
        for cluster_jewel in self.selected_cluster_jewels:
            if self.query == 1:
                notable_combinations = cluster_jewel['clusterNotables']
            else:
                # make a list of all possible combinations of items in each category
                notable_combinations = list(combinations(cluster_jewel['clusterNotables'], 2))
            lvlPrice = list()
            levels = list(cluster_jewel["clusterNotableLevels"].keys())
            for lvl in levels:
                if levels.index(lvl) == len(levels)-1:
                    maxLVL = 83
                else:
                    maxLVL = int(levels[levels.index(lvl)+1]) - 1
                x = {
                    'lvl': lvl,
                    'price': trade_api_utils.get_category_jewel_price(cluster_jewel, lvl, maxLVL)
                }
                lvlPrice.append(x)
            cluster_jewel['breakpointPrices'] = lvlPrice
            for notable_combination in notable_combinations:
                if self.query == 1:
                    min_lvl = notable_combination['notableLevel']
                else:
                    seq = [x['notableLevel'] for x in notable_combination]
                    min_lvl = max(seq)
                for item in cluster_jewel['breakpointPrices']:
                    if item['lvl'] == str(min_lvl):
                        jewel_price = item['price']
                        break
                notableData = trade_api_utils.getNotablePrice(cluster_jewel, notable_combination, self.query, self.inp, jewel_price)
                if notableData != 0:
                    all_averages.append(notableData)
                    self.data_updated.emit(all_averages)

        self.finished.emit()
