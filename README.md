Live demo: https://youtu.be/8doMJ0AG5c8?si=JPJqwq0sGP2lXV6c
# Lumibot-Alpaca News Trading App

## Overview
This application utilizes the Lumibot framework for algorithmic trading and integrates the Alpaca news API to make trades based on sentiment analysis of news data. The sentiment analysis is performed using the FinBERT model, which utilizes transformers and Python to predict the sentiment of news articles. The sentiment can be categorized as "positive", "negative", or "neutral", along with the probability of the sentiment being accurate.

## Trading Strategy
The trading strategy employed aims to maximize profits by making buy trades only when the news sentiment is positive and its probability exceeds 0.999. Conversely, sell trades are executed when the news sentiment is negative and its probability surpasses 0.999.

## Backtesting
To evaluate the effectiveness of the trading strategy, YahooDataBacktesting is utilized to simulate trades over a specified period. This allows for the calculation of potential profitability based on historical data.

## Technologies Used
- Lumibot: An easy-to-use algorithmic trading framework.
- Alpaca Trade API: Provides access to market data and allows for the placement of trades.
- FinBERT Model: Utilizes transformers and Python to perform sentiment analysis on news articles.
- YahooDataBacktesting: Enables backtesting of trading strategies using historical data from Yahoo Finance.

<img src="demoImages/trading strategy stats.png" alt="Alt Text" width="900">
<img src="demoImages/trading strategy map.png" alt="Alt Text" width="900">
<img src="demoImages/strategy stats.png" alt="Alt Text" width="900">


You can test the above by running `python tradingBot.py`.

## Part 2
To further make the project more realistic, I implemented a model to fetch real-time news from the Alpaca API, calculate the sentiment using the same FinBERT model, and make real-time trades if the sentiment was positive and the probability was more than 0.999. Market positions are closed if the sentiment was negative and the probability was more than 0.999. No action is taken if the sentiment was neutral.

To implement this, a node server was utilized, making websockets to communicate with the Alpaca live news API and a websocket to communicate with the Python server. Every time new news was received, it was sent to the Python server to calculate the sentiment and get it back on the Node server to implement the trading strategy logic.

Test the live news API and sentiment trading strategy by running `python receive.py` and then `node server.js`.

<img src="demoImages/positive example.png" alt="Alt Text" width="900">
<img src="demoImages/neutral example.png" alt="Alt Text" width="900">
