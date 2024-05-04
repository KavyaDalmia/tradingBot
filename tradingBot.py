from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime

from alpaca_trade_api import REST #we can dynamically get a bunch of stuff from this api
from datetime import timedelta

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
    def initialize(self, symbol:str="SPY", cash_at_rist:float=.5):
        # Initialize your strategy 
        self.symbol = symbol
        self.sleeptime = "5M"
        self.minutes_before_closing = 15
        self.last_trade = None # if you want to undo some of the last trades
        self.cash_at_risk = cash_at_rist
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)


    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0)
        #cash at risk of 0.5 means we using 50% of remaining cash to buy this stock.
        return cash, last_price, quantity

    def get_dates(self):
        today = self.get_datetime()
        three_days_before = today - timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_before.strftime('%Y-%m-%d')

    def get_news(self):
        # start will be 3 days prior and 
        # end is today
        today, three_days_before = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, 
                          start= three_days_before, 
                          end=today) #this returns a jumble, we are going to do processing on it 
        news = [ev.__dict__["_raw"]["headline"] for ev in news]
        return news

    def on_trading_iteration(self):
        # trading logic here
        cash, last_price, quantity = self.position_sizing()
        if cash > last_price: 
            if self.last_trade == None:
                news = self.get_news()
                print(news)
                order = self.create_order(
                    self.symbol,
                    quantity, 
                    "buy", 
                    type="bracket",
                    take_profit_price=last_price*1.2,
                    stop_loss_price=last_price*0.95
                    )
                #market or limit or what type of order is specified in type.
                #will run everytime we get new data
                self.submit_order(order)
                self.last_trade = "buy"


#create an instance of the strategy
strategy = MachineLearningTrader(name = 'mlstrat', broker= broker, parameters={"symbol": "SPY", "cash_at_risk": 0.2})

start_date = datetime(2024, 1, 15)
end_date = datetime(2024, 1, 30)

strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={"symbol":"SPY", "cash_at_risk": 0.2}
)

# notes:
# Lifecycle methods: Lifecycle methods are methods that are called by the trading engine at specific times.
# 