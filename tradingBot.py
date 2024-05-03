from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime

# lumibot is an easy algo trading framework
# alpaca-trade-api-python is to get news and place trades to broker
# datetime is to format dates
# timedelta is to calculate date differences
# torch - pytorch framework for using AI/ML
# transformers - to load up finance deep learning model


API_KEY = "PKKE8Q20HG91SIPFPQZA"
API_SECRET = "W1iXIc6aWZLmBKDuS7hUHlR9eay8bdKcT1rhJvmj"
BASE_URL = "https://paper-api.alpaca.markets/v2"
# link to get the api key: https://app.alpaca.markets/paper/dashboard/overview

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

broker = Alpaca(ALPACA_CREDS)

class MachineLearningTrader(Strategy):
    def initialize(self, symbol:str="SPY"):
        # Initialize your strategy 
        self.symbol = symbol
        self.sleeptime = "5M"
        self.minutes_before_closing = 15
        self.last_trade = None # if you want to undo some of the last trades
        
        pass
    def on_trading_iteration(self):
        # trading logic here
        if self.last_trade == None:
            order = self.create_order(self.symbol, 10, "buy", type="market")
            #market or limit or what type of order is specified in type.
            #will run everytime we get new data
            self.submit_order(order)
            self.last_trade = "buy"

#create an instance of the strategy
strategy = MachineLearningTrader(name = 'mlstrat', broker= broker, parameters={})

start_date = datetime(2024, 1, 15)
end_date = datetime(2024, 1, 30)

strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={"symbol":"SPY"}
)

# notes:
# Lifecycle methods: Lifecycle methods are methods that are called by the trading engine at specific times.
# 