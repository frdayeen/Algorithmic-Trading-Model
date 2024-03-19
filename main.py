import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import os
plt.style.use('ggplot')

sentiment_df = pd.read_csv('X_sentiment_data.csv')

sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])

sentiment_df = sentiment_df.set_index(['date','symbol'])

sentiment_df['eng_ratio'] = sentiment_df['X_Comments']/sentiment_df['X_Likes']

sentiment_df = sentiment_df[(sentiment_df['X_Likes']>20)&(sentiment_df['X_Comments']>10)]

# print(sentiment_df)


# Calculation of avg sentiment in the month
aggr_df = (sentiment_df.reset_index('symbol').groupby([pd.Grouper(freq='M'), 'symbol'])[['eng_ratio']].mean())

aggr_df['rank'] = (aggr_df.groupby(level=0)['eng_ratio'].transform(lambda x: x.rank(ascending=False)))


# top 10 stocks every month
top10_df = aggr_df[aggr_df['rank']<11].copy()

top10_df = top10_df.reset_index(level=1)

top10_df.index = top10_df.index+pd.DateOffset(1)

top10_df = top10_df.reset_index().set_index(['date', 'symbol'])

top10_df.head(10)


dates = top10_df.index.get_level_values('date').unique().tolist()

specific_dates = {}

for date in dates:
    specific_dates[date.strftime('%Y-%m-%d')] = top10_df.xs(date, level=0).index.tolist()

print(specific_dates)

#calculate portfolio returns with rebalancing

lists_stocks = sentiment_df.index.get_level_values('symbol').unique().tolist()

# print(lists_stocks)

stockPrice_df = yf.download(tickers=lists_stocks,
                            start='2021-01-01',
                            end='2023-03-01')

return_df = np.log(stockPrice_df['Adj Close']).diff().dropna()
# print(return_df)

portfolio_df = pd.DataFrame()

for startDate in specific_dates.keys():
    endDate = (pd.to_datetime(startDate)+pd.offsets.MonthEnd()).strftime('%y-%m-%d')

    columns = specific_dates[startDate]

    equalReturn_df = return_df[startDate:endDate][columns].mean(axis=1).to_frame('Portfolio_return')

    portfolio_df = pd.concat([portfolio_df, equalReturn_df], axis=0)

print(portfolio_df)
