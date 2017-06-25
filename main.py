import time
import os
import sys, getopt
import datetime
import json
from core import coin, coingraph, coinpair, poloniex

def main(argv):
    period=3
    pair = "BTC_BTS"
    prices = []
    currentMovingAverage = 0;
    lengthOfMA = 0
    startTime = False
    endTime = False
    historicalData = False
    tradePlaced = False
    typeOfTrade = False
    dataDate = ""
    orderNumber = ""

    try:
        opts, args = getopt.getopt(argv, 'hp:c:n:s:e:', ['period=','currenicy=','points='])
    except getopt.GetoptError:
        print 'main.py -p <period> -c <current pair> -n <period of moving average>'
        sys.exit(2)


    for opt, arg in opts:
        if opt=='-h':
            print 'main.py -p <period> -c <current pair>'
            sys.exit()
        elif opt in ('-p','--period'):
            if (int(arg)) in [3,300, 900, 1800, 720, 14400, 86400]:
                period = arg
            else:
                print 'Poloniex require periods 3, 300, 900, 1800, 720, 14400, 86400 increments'
                sys.exit(2)
        elif opt in ('-c', '--currency'):
            pair = arg
	elif opt in ("-n", "--points"):
            lengthOfMA = int(arg)
	elif opt in ("-s"):
	    startTime = arg
	elif opt in ("-e"):
	    endTime = arg

    conn = poloniex.poloniex('Key1','Key2')
    curPair = coinpair.CoinPair()

    
    while True:
        print '******************************'

        curPair.add_coin('BTC_SC',conn)
        startTime=datetime.datetime(2015, 01, 01, 12, 00, 00)
        endTime=datetime.datetime(2017, 06, 20, 12, 00, 00)
        curPair.get_historical_data(startTime,endTime,14400,True)
        sys.exit()


        #ticker = conn.api_query('returnTicker')
        #coins.read_from_ticker(ticker)
        #coins.print_coins(coinType='usd')
        #coins.print_coins(name='BTS')
        #coins.find_arbitrage_opportunity()
        #tradeName='BTC_ETH'
        #lastPrice=float(coins.ticker[tradeName]['last'])
        #print lastPrice
        #amount=0.00012/lastPrice/1.01
        #print amount,lastPrice*1.01
        #print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #orderNumber = conn.buy(tradeName,lastPrice*1.01,amount)
        #print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #for key,item in orderNumber['resultingTrades'][0].items():
        #    print key, item
        #print orderNumber
        #exit()
        time.sleep(int(period))
        continue

if __name__== '__main__':
    main(sys.argv[1:])
