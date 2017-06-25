import urllib
import urllib2
import json
import time
import hmac,hashlib
from poloniex import poloniex


MAX_PATH_SIZE=5
MIN_PATH_SIZE=3
START_VALUE=1000
TRIGGER_THRESHOLD=0.02
COIN_RANK=['ETH','ETC','XRP','NXT','DGB','DASH','LTC','ZEC','SC','STRAT','FCT','XEM','LSK','STR','GNT','GNO','STEEM']
COIN_RANK_COPY=['ETH','BTS','ETC','XRP','NXT','DGB','DASH','LTC','ZEC','SC','STRAT','FCT','XEM','LSK','XMR','STR','GNT','DOGE','STEEM','SYS','POT','DCR','ARDR','GRC','BLK','REP','BCN','GNO']

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

class CoinGraph:
    def __init__(self):
        self.graph={}
        self.masterCoinGraph={}
        self.altCoinGraph={}
        self.usdCoinGraph={}
        self.ticker={}
        self.poloniexBot=None

    def add_coin(self, coin):
        self.graph[coin.name]=coin

    def get_coin(self, name):
        return self.graph.get(name)

    def read_from_ticker(self, ticker):
        for key, item in ticker.items():
            names=key.split('_')
            price=item['last']
            baseVolume=item['baseVolume']
            if baseVolume<=2000:
                continue
            for name in names:
                if not self.get_coin(name):
                    self.add_coin(Coin(name))
            self.graph[names[0]].add_edge(names[1], 1/float(price))
            if names[0]<>'USDT':
                self.graph[names[1]].add_edge(names[0],float(price))
        self.ticker=ticker
        self.update_other_coin_graph()

    def update_other_coin_graph(self):
        self.masterCoinGraph={}
        self.altCoinGraph={}
        self.usdCoinGraph={}
        for name,coin in self.graph.items():
            if coin.coinType=='master':
                self.masterCoinGraph[name]=coin
            elif coin.coinType=='usd':
                self.usdCoinGraph[name]=coin
            else:
                self.altCoinGraph[name]=coin
            
    def print_coins(self, name=None, coinType=None):
        tmpGraph={}
        if name:
            if not self.graph[name]:
                return 'None such coin: '+name
            tmpGraph[name]=self.graph[name]
        elif coinType is not None:
            if coinType=='master':
                tmpGraph=self.masterCoinGraph
            elif coinType=='usd':
                tmpGraph=self.usdCoinGraph
            else:
                tmpGraph=self.altCoinGraph
        else:
            tmpGraph=self.graph
        for name,coin in tmpGraph.items():
            print coin.name, coin.coinType, coin.edges

    def find_arbitrage_opportunity(self):
        possiblePath=[[node]+path  for node in ['BTC','ETH'] for path in self.dfs(node,node)]
        possibleSet=[]
        finalPath=[]
        for path in possiblePath:
            if 'XMR' in path:
                continue
            if self.get_arbitrage_return(path)>=TRIGGER_THRESHOLD:
                if set(path) in possibleSet:
                    continue
                possibleSet.append(set(path))
                print '------------------------------'
                print "GAIN : ",round(self.get_arbitrage_return(path),3), path
                curr=path[0]
                for name in path[1:]:
                    print curr,':',name, ':', self.graph[curr].edges[name]
                    curr=name
                print 
        return finalPath

    def dfs(self,start,end):
        fringe=[(start,[])]
        while fringe:
            state,path=fringe.pop()
            if path and state == end:
                if len(path)>MIN_PATH_SIZE-1 and len(path)<=MAX_PATH_SIZE:
                    yield path
                continue
            for next_state in self.graph[state].edges.keys():
                if next_state in path:
                    continue
                fringe.append((next_state,path+[next_state]))

    def get_arbitrage_return(self,path):
        curr=path[0]
        value=START_VALUE
        for name in path[1:]:
            value=value*self.graph[curr].edges[name]
            curr=name
        return value/START_VALUE-1

    def setupPoloniexBot(self, poloniexBot):
        self.poloniexBot=poloniexBot

class PoloniexBot:
    def __init__(self, apiKey, secret):
        self.conn = poloniex(apiKey, secret)

    def trade_arbitrage_path(self, path, ticker):
        return 
