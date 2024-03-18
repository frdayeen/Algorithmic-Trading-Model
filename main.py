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


print(aggr_df)