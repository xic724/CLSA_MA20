import random

import BaseType.MarketData as MarketData

## 5 HK market data cache
class MarketDataHandler():
    def __new__(self):
        self.MarketDataCache5HK = dict()
        for i in range(1, 100):
            MarketData5HK = self.generateMarketDataCache()
            self.MarketDataCache5HK[i] = MarketData5HK

    def __init__(self):
        pass

    def generateMarketDataCache():
        MarketData5HK = MarketData()
        MarketData5HK.BlpCode = "5 HK"
        MarketData5HK.RicCode = "5.HK"
        MarketData5HK.ISINCode = "A1B2C3D4"
        MarketData5HK.SEDOLCode = "123456789"
        MarketData5HK.ExchangeCode = "HK"
        
        # for the sake of argument...
        MarketData5HK.Bid = random() 
        MarketData5HK.Ask = MarketData5HK.Bid + random()
        return MarketData5HK

    def getBid(self, i):
        return self.MarketDataCache5HK[i].Bid

    def getAsk(self, i):
        return self.MarketDataCache5HK[i].Ask
        