import urllib
import urllib2
import json
import time
import hmac,hashlib
from poloniex import poloniex

class Coin:
    def __init__(self, name):
        self.name = name
        self.coinType = 'alt'
        if self.name in ['BTC','ETH','XMR']:
            self.coinType = 'master'
        elif self.name == 'USDT':
            self.coinType = 'usd'
        self.edges = {}

    def add_edge(self, neighbourName, price):
        self.edges[neighbourName]=price
