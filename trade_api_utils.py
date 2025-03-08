import math
import statistics
import requests
import time
from json import loads as load
import json

headers = requests.utils.default_headers()

#Current rate-limit header rules: 5:10:60,15:60:300,30:300:1800

headers.update({
    'User-Agent': "IDareYouLV's cluster notable combination price checker",
    'From': 'arturino009@gmail.com'
})
cookies = {
    "POESESSID": "your_poe_session_id"
}

def getLeague(league_id):
    leagues = requests.get('http://api.pathofexile.com/leagues', headers=headers)
    leagues = leagues.json()
    current_league = leagues[league_id]['id']  # current challenge league
    return current_league


def getCurrencies(league):
    response = requests.get(
        'https://poe.ninja/api/data/currencyoverview?league=' + current_league + '&type=Currency', headers=headers)
    currencies = load(response.text)['lines']
    rates = {
        c['currencyTypeName']: c['chaosEquivalent'] for c in currencies
    }
    with open('currency.json') as json_file:
        currShort = json.load(json_file)
    arr = []
    for name in currShort:
        for name_a in rates:
            if name == name_a:
                x = {
                    'currFull': name,
                    'curr': currShort[name],
                    'rate': rates[name]
                }
                arr.append(x)
    return arr

class RateLimitedRequester:
    def __init__(self):
        # Optional headers/cookies that can be passed in.
        self.headers = headers
        self.cookies = cookies
        # These dictionaries persist across requests.
        self.global_window_start_times = {}
        self.account_window_start_times = {}

    def get_rate_limit_headers(self, response):
        # If your API doesn't supply these headers, replace the default values as needed.
        return {
            "global_limit": response.headers.get("X-Rate-Limit-Ip", "8:10:60,15:60:120,60:300:1800"),
            "global_state": response.headers.get("X-Rate-Limit-Ip-State", "0:10:0,0:60:0,0:300:0"),
            "account_limit": response.headers.get("X-Rate-Limit-Account", "8:10:60,15:60:120,60:300:1800"),
            "account_state": response.headers.get("X-Rate-Limit-Account-State", "0:10:0,0:60:0,0:300:0")
        }

    def calculate_delay(self, rate_limit_rules, rate_limit_state, window_start_times):
        """
        For each rule:
          - If the burst limit is not yet reached, no delay is needed.
          - If the limit is reached, we wait until the current window resets.
          - If a penalty is active, we wait for that penalty.
        """
        # Parse the rules and state into lists of tuples.
        rules = [tuple(map(int, rule.split(':'))) for rule in rate_limit_rules.split(',')]
        states = [tuple(map(int, state.split(':'))) for state in rate_limit_state.split(',')]
        delays = []
        now = time.time()
        for idx, (rule, state) in enumerate(zip(rules, states)):
            max_requests, timeframe, penalty_time = rule
            requests_made, state_timeframe, remaining_penalty = state

            # Get or initialize the window start time.
            window_start = window_start_times.get(idx, now)
            elapsed = now - window_start

            # If a penalty is active, enforce that delay.
            if remaining_penalty > 0:
                delays.append(remaining_penalty)
                continue

            if requests_made < max_requests:
                # Still below the limit – no delay needed.
                delay = 0
            else:
                # If the limit is reached, wait until the window resets.
                delay = max(0, timeframe - elapsed)
                formatted_time = time.strftime('%H:%M:%S', time.localtime(window_start))
                print("Window start time:", formatted_time)
                formatted_time_now = time.strftime('%H:%M:%S', time.localtime(window_start))
                print("Time now:", formatted_time_now)
            delays.append(delay)
        
        # To be safe, use the most restrictive delay among all rules.
        return max(delays) if delays else 0

    def update_window_times(self, rate_limit_rules, window_start_times, last_request_time):
        """
        For each rule:
          - If no window start time exists, initialize it to last_request_time.
          - Otherwise, if the window has expired, update it to last_request_time.
        """
        rules = [tuple(map(int, rule.split(':'))) for rule in rate_limit_rules.split(',')]
        for idx, (max_requests, timeframe, _) in enumerate(rules):
            if idx not in window_start_times:
                window_start_times[idx] = last_request_time
            else:
                if last_request_time - window_start_times[idx] >= timeframe:
                    window_start_times[idx] = last_request_time


    def send_request(self, url, data=None):
        last_request_time = None
        while True:
            current_time = time.time()
            elapsed_since_last = current_time - last_request_time if last_request_time else 0

            if data:
                response = requests.post(url, json=data, headers=self.headers, cookies=self.cookies)
            else:
                response = requests.get(url, headers=self.headers, cookies=self.cookies)

            rate_limits = self.get_rate_limit_headers(response)
            print("Rate limits:", rate_limits)

            global_delay = self.calculate_delay(rate_limits["global_limit"],
                                                rate_limits["global_state"],
                                                self.global_window_start_times)
            account_delay = self.calculate_delay(rate_limits["account_limit"],
                                                 rate_limits["account_state"],
                                                 self.account_window_start_times)
            delay = max(global_delay, account_delay)
            print("Calculated delay:", delay)

            response_json = response.json()
            if 'error' in response_json:
                print("Error:", response_json['error']['message'])
                time.sleep(delay)
                continue

            last_request_time = time.time()

            # Update the window start times (this call now passes 3 arguments plus self)
            self.update_window_times(rate_limits["global_limit"],
                                     self.global_window_start_times,
                                     last_request_time)
            self.update_window_times(rate_limits["account_limit"],
                                     self.account_window_start_times,
                                     last_request_time)

            if delay > elapsed_since_last:
                time.sleep(delay - elapsed_since_last)
            return response_json


# Small breakpoints: 1-49; 50-67; 68-72; 75-77
# Medium breakpoints: 1-49; 50-67; 68-74; 75-83  //not all have 75 notables, so they have 68-83 breakpoint

def get_category_jewel_price(a, ilvl, maxlvl):
    data_set = {  # structure for API request. All info from https://www.reddit.com/r/pathofexiledev/comments/7aiil7/how_to_make_your_own_queries_against_the_official/ . Absolutely no other documentation
        "query": {
            "status": {
                "option": "online"
            },
            "stats": [{
                "type": "and",
                "filters": [{"id": 'enchant.stat_3948993189', "value": {"option": a['clusterId']}},
                            {"id": "enchant.stat_3086156145", "value": {"max": 5}}]
            }],
            "filters": {
                "type_filters": {
                    "filters": {
                        "rarity": {
                            "option": "nonunique"
                        }
                    }
                },
                "misc_filters": {
                    "filters": {
                        "corrupted": {
                            "option": "false"
                        },
                        "ilvl": {
                            "min": ilvl,
                            "max": maxlvl
                        }
                    }
                },
                "trade_filters": {
                    "filters": {
                        "sale_type": {
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
    # send the request to API
    response = requester.send_request('https://www.pathofexile.com/api/trade/search/' + current_league, data_set)
    result = response['result']
    id = response['id']
    size = response['total']
    if size == 0:
        return 0
    # if there are more than 10 listings, strip all of them away after 10th. We cant request info about items more than 10 items at once
    if size > 10:
        del result[10:]

    # make correct formatting
    if size > 1:
        str1 = ','.join(result)
    else:
        str1 = result

    # get all actual listings of items
    address = 'https://www.pathofexile.com/api/trade/fetch/' + \
        str(str1) + '?query=' + id
    results_json = requester.send_request(address)
    # list to hold all prices of an item. Later used to calculate medium price
    medium = list()
    #print("Address: " + address)
    print("Base: " + a['clusterName'])
    print("ilvl: " + str(ilvl) + "-" + str(maxlvl))
    print('Listings:' + str(size))
    for p in results_json['result']:
        # conversion for some more valuable currency
        currency = p['listing']['price']['currency']
        if currency != 'chaos' or currency == 'p':
            try:
                curr = [dictionary for dictionary in rates if dictionary["curr"]
                        == p['listing']['price']['currency']]
                p['listing']['price']['amount'] = p['listing']['price']['amount'] * curr[0]['rate']
                p['listing']['price']['currency'] = "chaos"
            except:
                continue
        medium.append(p['listing']['price']['amount'])
    # get the average median of all listed prices for an item
    if medium == 0:
        avg = 1
    else:
        avg = statistics.median_grouped(medium)
    print("Average median price: " + str(round(avg, 2)) + '\n')
    return avg


def getNotablePrice(cluster_jewel, notable_combination, query, inp, jewel_price):
    if query == 1:
        ilvl = notable_combination['notableLevel']
    else:
        ilvl = max(notable_combination[0]['notableLevel'], notable_combination[1]['notableLevel'])

    data_set = {  # structure for API request. All info from https://www.reddit.com/r/pathofexiledev/comments/7aiil7/how_to_make_your_own_queries_against_the_official/ . Absolutely no other documentation
        "query": {
            "status": {
                "option": "online"
            },
            "type": "Small Cluster Jewel" if inp == 1 else "Medium Cluster Jewel",
            "stats": [{
                "type": "and",
                "filters": [{"id": notable_combination['notableId']}] if query == 1 else [{"id": notable_combination[0]['notableId']}, {"id": notable_combination[1]['notableId']},
                                                                                          {"id": "enchant.stat_3086156145", "value": {"max": 5}}]
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
                    "filters": {
                        "sale_type": {
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
    # send the request to API
    response = requester.send_request('https://www.pathofexile.com/api/trade/search/' + current_league, data_set)
    result = response['result']
    id = response['id']
    size = response['total']

    # if there are less than 10 listings for an item, we just just skip it (no demand)
    if size < 10:
        print("Not enough items!(" + str(size) + ") Skipping... " + (notable_combination['notableName'] if query == 1 else (notable_combination[0]['notableName'] + " and " + notable_combination[1]['notableName'])) +"\n")
        return 0

    # if there are more than 10 listings, strip all of them away after 10th. We cant request info about items more than 10 items at once
    if size > 10:
        del result[10:]

    # make correct formatting
    if size > 1:
        str1 = ','.join(result)
    else:
        str1 = result

    # get all actual listings of items
    address = 'https://www.pathofexile.com/api/trade/fetch/' + \
        str(str1) + '?query=' + id
    results_json = requester.send_request(address)

    # probability to get an item while crafting. Formula is mostly correct
    altPrice = [dictionary for dictionary in rates if dictionary["currFull"]
                == "Orb of Alteration"][0]['rate']
    augPrice = [dictionary for dictionary in rates if dictionary["currFull"]
                == "Orb of Augmentation"][0]['rate']

    clusterPrefixWeight = cluster_jewel['clusterWeightPrefix']      #lvl83 -2100 medium -900 small
    weight75 = 900 if inp == 1 else 2100
    weight68 = (cluster_jewel['clusterNotableLevels'][75] if 75 in cluster_jewel['clusterNotableLevels'] else 0) + weight75 + (1200 if inp == 1 else 0)
    weight50 = (cluster_jewel['clusterNotableLevels'][68] if 68 in cluster_jewel['clusterNotableLevels'] else 0) + weight68 + (4200 if inp == 1 else 2400)
    weight1 = (cluster_jewel['clusterNotableLevels'][50] if 50 in cluster_jewel['clusterNotableLevels'] else 0) + weight50

    weights = {
        "1" : weight1,
        "50" : weight50,
        "68" : weight68,
        "75" : weight75,
        "84" : weight75,
    }

    clusterPrefixWeight = clusterPrefixWeight - weights[str(ilvl)]

    if query == 1:
        probability = notable_combination['notableWeight']/clusterPrefixWeight
        tries = math.ceil(1 / probability)
        alt_count = tries
        aug_count = math.ceil(alt_count/4)
        craft_price = alt_count * altPrice + aug_count * augPrice

    else:
        regalPrice = [
            dictionary for dictionary in rates if dictionary["currFull"] == "Regal Orb"][0]['rate']
        scourPrice = [dictionary for dictionary in rates if dictionary["currFull"]
                      == "Orb of Scouring"][0]['rate']
        transPrice = [dictionary for dictionary in rates if dictionary["currFull"]
                      == "Orb of Transmutation"][0]['rate']

        suffixWeight = 14150

        sweight75 = 1100 if inp == 1 else 3550
        sweight68 = sweight75 + (2200 if inp == 1 else 0)
        sweight50 = sweight68 + (7700 if inp == 1 else 4750)
        sweight1 = sweight50

        sweights = {
        "1" : sweight1,
        "50" : sweight50,
        "68" : sweight68,
        "75" : sweight75,
        "84" : sweight75
        }   

        suffixWeight = suffixWeight - sweights[str(ilvl)]

        probabilityFirst = notable_combination[0]['notableWeight'] / clusterPrefixWeight
        probabilityFirstSecond = notable_combination[1]['notableWeight'] / \
            (clusterPrefixWeight + suffixWeight - notable_combination[0]['notableWeight'])
        probabilityFirstSucess = probabilityFirst * probabilityFirstSecond

        probabilitySecond = notable_combination[1]['notableWeight'] / clusterPrefixWeight
        probabilitySecondFirst = notable_combination[0]['notableWeight'] / \
            (clusterPrefixWeight + suffixWeight - notable_combination[1]['notableWeight'])
        probabilitySecondSucess = probabilitySecond * probabilitySecondFirst

        probability = probabilityFirstSucess + \
            probabilitySecondSucess  # overall probability to hit both

        probability_first = (notable_combination[0]['notableWeight'] + notable_combination[1]
                             ['notableWeight']) / clusterPrefixWeight
        probability_second = probability/probability_first

        tries = math.ceil(1 / probability)
        regal_count = math.ceil(1 / probability_second)
        scour_count = regal_count - 1
        trans_count = regal_count - 1
        alt_count = tries - trans_count
        aug_count = math.ceil((tries + alt_count) / 4) + 1
        craft_price = alt_count * altPrice + aug_count * augPrice + regal_count * \
            regalPrice + scour_count * scourPrice + trans_count * transPrice

    craft_and_jewel_price = craft_price + jewel_price

    # list to hold all prices of an item. Later used to calculate medium price
    medium = list()

    if query == 1:
        print(notable_combination['notableName'] + ": " + str(round(probability*100, 3)) + "%" +
              " Cost for rerolls: " + str(round(craft_price, 2)) + " Tries: " + str(round(tries)))
        print('Listings:' + str(size))
    else:
        print(notable_combination[0]['notableName'] + " and " + notable_combination[1]['notableName'] + ": " + str(round(probability*100, 3)
                                                                               ) + "%" + " Cost for rerolls: " + str(round(craft_price, 2)) + " Tries: " + str(round(tries)))
        print('Listings:' + str(size) + " Weight: " + str(clusterPrefixWeight))

    for p in results_json['result']:
        # conversion for some more valuable currency
        currency = p['listing']['price']['currency']
        if currency != 'chaos' or currency == 'p':
            try:
                curr = [dictionary for dictionary in rates if dictionary["curr"]
                        == p['listing']['price']['currency']]
                price = p['listing']['price']['amount'] * curr[0]['rate']
                p['listing']['price']['amount'] = price
                p['listing']['price']['currency'] = "chaos"
            except:
                continue
        medium.append(p['listing']['price']['amount'])
        print("Price: ", p['listing']['price']['amount'],
              " ", p['listing']['price']['currency'], '\n')

    # get the average median of all listed prices for an item
    avg = statistics.median_grouped(medium)
    # profit margin
    profit = avg - craft_and_jewel_price
    PPT = profit/tries
    if len(medium) > 1:
        first = (medium[0]+medium[1])/2
    else:
        first = medium[0]
    LPPT = (first - craft_and_jewel_price)/tries
    print("The average median is ", round(avg, 2),
          "     Profit:", round(profit, 2), '\n')
    x = {
        'name': notable_combination['notableName'] if query == 1 else (notable_combination[0]['notableName'] + " and " + notable_combination[1]['notableName']),
        'listings': size,
        'tries': round(tries),
        'craft_price': round(craft_price, 2),
        'first': round(first, 2),
        'average_price': round(avg, 2),
        'profit': round(profit, 2),
        'PPT': round(PPT, 3),
        'LPPT': round(LPPT, 3), # when first item is a lot cheaper than average
        'category': cluster_jewel['clusterName'],
        'request': data_set,
        'category_full': cluster_jewel,
        'notable_full': notable_combination,
        'ilvl': ilvl,
        'id': id
    }
    return x
# 8 is default
# 16 is event 
current_league_id = 16
current_league = getLeague(current_league_id)

print("Current league : " + current_league)

rates = getCurrencies(current_league)

requester = RateLimitedRequester()
