import BaseType.InstrumentRestriction as Restriction

## 5 HK instrument restriction cache
class RiskParamHandler():
    def __new__(self):
        self.InstrumentRestrictionDict = dict()
        instrumentRestriction = Restriction()
        instrumentRestriction.BlpCode = "5 HK"
        instrumentRestriction.RicCode = "5.HK"
        instrumentRestriction.ISINCode = "A1B2C3D4"
        instrumentRestriction.SEDOLCode = "123456789"
        instrumentRestriction.ExchangeCode = "HK"
        instrumentRestriction.BlockMarket = True
        instrumentRestriction.BlockClient = True
        instrumentRestriction.BlockAccount = True

        self.InstrumentRestrictionDict[instrumentRestriction.BlpCode, instrumentRestriction]

    def __init__(self):
        pass

    def validateOrder(newOrder):
        ##TODO
        ## Validate Instrument eligible to trade
        return True
        
