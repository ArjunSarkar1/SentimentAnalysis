from datetime import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# NLTK
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

# Matplotlib Library
import matplotlib.pyplot as plt

finviz_url = "https://finviz.com/quote.ashx?t="
ticker_symbols = ['IBM','ACN','ADBE','UBER']
# ticker_symbols = ['GOOG','META','AMZN']

news_tables = {} 

for ticker in ticker_symbols:
    url = finviz_url + ticker

    # making a request to acquire html data from the above urls
    req = Request(url=url, headers={'user-agent': 'test-app'})
    response = urlopen(req)
    
    html_output = BeautifulSoup(response, features='html.parser')
    tables = html_output.find(id="news-table")
    news_tables[ticker] = tables

# Parsed Data List consists of:
# - Ticker Symbol
# - Date
# - Time
# - News Headline 
all_parsed_data = []

for ticker, news in news_tables.items():

    for rows in news.findAll('tr'):
        headlines = rows.a.text.strip()
        date_time = rows.td.text.strip().split(' ')
        headline_link = rows.findAll('td')[1].a['href']

        if len(date_time) > 1:
            date = date_time[0]
            if date == 'Today':
                date = datetime.now().date()
            else:
                date = pd.to_datetime(date).date()
            time = date_time[1]
        else:
            date = pd.to_datetime(date_time[0]).date()
            time = ''

        all_parsed_data.append([ticker, date, time, headlines])

# Creating DataFrame from parsed data
data_frame = pd.DataFrame(all_parsed_data, columns=['Ticker', 'Date', 'Time', 'Headlines'])

# Initializing VADER sentiment analyzer
vader = SentimentIntensityAnalyzer()
function = lambda headlines: vader.polarity_scores(headlines)['compound']

# Calculating sentiment score for each headline
data_frame['compound'] = data_frame['Headlines'].apply(func=function)

# Grouping by date and ticker, calculating the average sentiment score
sentiment_trend = data_frame.groupby(['Date', 'Ticker'])['compound'].mean().unstack()

print(sentiment_trend.head())

#----------------#
# Bar Chart
#----------------#

# Plot the sentiment trend using Pandas plot function
sentiment_trend.plot(kind='bar', figsize=(11, 7))

plt.title('Sentiment Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Average Sentiment Score')
plt.legend(title='Ticker')
plt.grid(True)
plt.show()

#----------------#
# Trend Line
#----------------#

# # Plotting
# plt.figure(figsize=(11, 5))

# # Iterate over each company and plot its sentiment trend
# for ticker in ticker_symbols:
#     plt.plot(sentiment_trend.index, sentiment_trend[ticker], label=ticker)

# plt.title('Sentiment Trend Over Past Four Days')
# plt.xlabel('Date')
# plt.ylabel('Average Sentiment Score')
# plt.legend()
# plt.grid(True)
# plt.show()
