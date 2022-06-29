import requests
import json
from datetime import date


class Report:
    def __init__(self):
        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        self.params = {
            'start': '1',
            'limit': '100',
            'convert': "USD"
        }

        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'cbd962a8-1544-4c2c-89f1-98a18db9f2a1'
        }

    def fetchCurrentData(self):
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        return r['data']


report = Report()
data = report.fetchCurrentData()


def max_volume(data):
    volumes = {v['quote']['USD']['volume_24h']: v['name'] for v in data}
    return volumes[max(volumes)]  #


def best_and_worst_currencies(data):
    currencies = {v['quote']['USD']['percent_change_24h']: v['name'] for v in data}

    sorted_currencies = sorted(currencies)
    best_currencies = sorted_currencies[:10]
    worst_currencies = sorted_currencies[-10:]
    best = []
    worst = []
    for v, name in currencies.items():
        if v in best_currencies:
            best.append(name)
        if v in worst_currencies:
            worst.append(name)
    return best, worst


def first_20_curriences(data):
    curriences = {c['name']: c['quote']['USD']['price'] for c in data[:20]}
    return curriences


def money_to_buy_max_24h_volume_currency(data, volume):
    prices = {v['name']: v['quote']['USD']['price'] for v in data
               if v['quote']['USD']['volume_24h'] > volume}
    return prices


def first_20_curriences_percentage_change_24h(data):
    percentage_change_24h = {p['name']: p['quote']['USD']['percent_change_24h'] for p in data[:20]}
    return percentage_change_24h


# find the percentage of gain or loss I have if I bought one unit of each
# of the top 20 cryptocurrencies the day before
def find_percentage(data):
    new_20 = first_20_curriences_percentage_change_24h(data)
    margin = (sum(new_20.values()))
    return margin


# write the output on the file with today's date
today = date.today()
max_volume_crypto = max_volume(data)
bests, worsts = best_and_worst_currencies(data)
f_20 = first_20_curriences(data)
price_max24h_volume_currency = money_to_buy_max_24h_volume_currency(data, 76000000)
percentage = find_percentage(data)
result = {'max_volume_crypto': max_volume_crypto,
          'bests': bests,
          'worst': worsts,
          'first_20_crypto': f_20,
          'crypto': price_max24h_volume_currency,
          'margin': percentage}
with open(f"{today}.json", "w") as outfile:
    json.dump(result, outfile, indent=4)
