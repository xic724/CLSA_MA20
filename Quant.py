import os
import sys
import math
import datetime
import traceback

import numpy as np
import pandas as pd
import scipy as sp
import yfinance as yf

from BaseType.Config import Config
from BaseType.Logger import Logger

from ModelHandler.AlphaResearchHandler import AlphaResearchHandler
from ModelHandler.DownloadHandler import DownloadHandler
from ModelHandler.AlphaResearchHandler import AlphaResearchHandler
from ModelHandler.PnLAttributionHandler import PnLAttributionHandler
from ModelHandler.RiskParamHandler import RiskParamHandler
from ModelHandler.NewOrderHandler import NewOrderHandler

class Quant():
    def __init__(self):
        Config.LoadConfigFile()
        Logger(__file__, True)

    def run(self):
        Logger.INFO("Running Quant project...")

        #downloadHandler = DownloadHandler()
        #marketData = downloadHandler.downloadData()

        # alphaResearchHandler = AlphaResearchHandler()
        # alphaResearchHandler.analyzeData()

        # newOrderHandlerHandler = NewOrderHandler()
        # newOrderHandlerHandler.createNewOrder()    

        # riskParamHandler = RiskParamHandler()
        # riskParamHandler.validateOrder()

        # pnLAttributionHandler = PnLAttributionHandler()
        # pnLAttributionHandler.attributePnL()

        
        
        # for simplicity, just write code here in Quant.py
        marketData = downloadData('AAPL')
        ma20Data = analyzeData(marketData)
        ma20DataBenchmark = createBenchmark(ma20Data)
        createSignal(ma20DataBenchmark)
        plotReturn(ma20DataBenchmark)

        # next, extrapolate MA20 strategy on SP100 NAV
        SP100 = ['AAPL', 'ABBV', 'ABT', 'ACN', 'ADBE', 'AIG', 'AMGN', 'AMT', 'AMZN', 'AVGO', 'AXP', 'BA', 'BAC', 'BK', 'BKNG', 'BLK', 'BMY', 'BRK.B', 'C', 'CAT', 'CHTR', 'CL', 'CMCSA', 'COF', 'COP', 'COST', 'CRM', 'CSCO', 'CVS', 'CVX', 'DD', 'DHR', 'DIS', 'DOW', 'DUK', 'EMR', 'EXC', 'F', 'FDX', 'GD', 'GE', 'GILD', 'GM', 'GOOG', 'GOOGL', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'KHC', 'KO', 'LIN', 'LLY', 'LMT', 'LOW', 'MA', 'MCD', 'MDLZ', 'MDT', 'MET', 'META', 'MMM', 'MO', 'MRK', 'MS', 'MSFT', 'NEE', 'NFLX', 'NKE', 'NVDA', 'ORCL', 'PEP', 'PFE', 'PG', 'PM', 'PYPL', 'QCOM', 'RTX', 'SBUX', 'SCHW', 'SO', 'SPG', 'T', 'TGT', 'TMO', 'TMUS', 'TSLA', 'TXN', 'UNH', 'UNP', 'UPS', 'USB', 'V', 'VZ', 'WBA', 'WFC', 'WMT', 'XOM']
        
        marketDataDict = dict()
        marketDataDict = downloadData(SP100)
        print(marketDataDict.head(20))
        #print(marketDataDict['Adj Close'].head(20))
        #marketDataDict = analyzeData(marketDataDict)

        #### 2:15hr - take a break here to retrospect
        ####   1. To compute NAV, must construct the SP100 weight vector (SP100 is float-adjusted market capitalization)
        ####   2. To popluate MA20 column on SP100, must pool the Adj Close of 100 consituents together
        ####   ...

def downloadData(instrumentList):
    marketData = yf.download(tickers=instrumentList, start="2021-01-01", end="2021-04-30")
    #print(marketData.head(3))
  
    return marketData


def analyzeData(marketData):
    #create moving average 20days column with upper/lower bands in 1 standard deviation
    marketData['ma20'] = marketData['Adj Close'].rolling(window=20).mean()
    marketData['std'] = marketData['Adj Close'].rolling(window=20).std()
    marketData['Upper_Band'] = marketData['ma20'] + (1 * marketData['std'])
    marketData['Lower_Band'] = marketData['ma20'] - (1 * marketData['std'])
    
    #print(marketData.head(50))
    return marketData

def createBenchmark(ma20Data):
    #compute daily return of buy and hold strategy as a benchmark (in log scale)
    ma20Data['Buy_Hold'] = np.log(ma20Data['Adj Close']/ma20Data['Adj Close'].shift(1))
    return ma20Data

def createSignal(ma20Data):
    # BUY if Adj Close moves underneath Lower_Band and mean reversal on T+1
    ma20Data['Signal'] = np.where(
        (ma20Data['Adj Close'] < ma20Data['Lower_Band']) & (ma20Data['Adj Close'].shift(1) >= ma20Data['Lower_Band']), 1, 0)

    # SELL if Adj Close moves beyond Upper_Band and mean reversal on T+1
    ma20Data['Signal'] = np.where(
        (ma20Data['Adj Close'] > ma20Data['Upper_Band']) & (ma20Data['Adj Close'].shift(1) <= ma20Data['Upper_Band']), -1, ma20Data['Signal'])

    # creating L/S Positions
    # if qty is 0, no action today. Take the prev day position: "1" is Long, "-1" is short
    ma20Data['Position'] = ma20Data['Signal'].replace(to_replace=0, method='ffill').shift(1)

    # calculating returns of MA20 for each day
    ma20Data['MovingAvg'] = ma20Data['Buy_Hold'] * (ma20Data['Position'])

    #print(ma20Data.tail(50))

def plotReturn(ma20Data):
    ma20Data[['Buy_Hold','MovingAvg']] = ma20Data[['Buy_Hold','MovingAvg']].cumsum()
    ma20Data[['Buy_Hold','MovingAvg']].plot(grid=True)


if __name__ == "__main__":
    try:
        quant = Quant()
        quant.run()
    except:
        Logger.ERROR(str(traceback.format_exc()))