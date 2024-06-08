import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, Time

my_engine = create_engine('sqlite:///my_news.db')
my_base = declarative_base()

class MyNews(my_base):
    __tablename__ = 'News_Headlines'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    ticker = Column(String)
    headlines = Column(String)
    sentimentScore = Column(Float)

Session = sessionmaker(bind=my_engine)
sesh = Session()

# Base URL and ticker symbols
finviz_url = "https://finviz.com/quote.ashx?t="
ticker_symbols = ['IBM', 'ACN', 'ADBE', 'UBER']

news_tables = {}

# Fetching data for each ticker
for ticker in ticker_symbols:
    url = finviz_url + ticker
    try:
        # Fetching data from a URL
        req = Request(url=url, headers={'user-agent': 'test-app'})
        response = urlopen(req)
        html_output = BeautifulSoup(response, features='html.parser')
        tables = html_output.find(id="news-table")
        news_tables[ticker] = tables
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")

# Parsed Data List
all_parsed_data = []

# Iterating over the items in the `news_tables` dictionary, where each item
# consists of a ticker symbol as the key and the corresponding news table as the value.
for ticker, news in news_tables.items():
    if news is not None:
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

# Creating a Data Frame
data_frame = pd.DataFrame(all_parsed_data, columns=['Ticker', 'Date', 'Time', 'Headlines'])

#-----------------------------------------------------------
# Applying Sentiment Analysis
#-----------------------------------------------------------

# Initializing VADER sentiment analyzer
vader = SentimentIntensityAnalyzer()
function = lambda headlines: vader.polarity_scores(headlines)['compound']
data_frame['compound'] = data_frame['Headlines'].apply(function)

# Insert data into the database
for _, row in data_frame.iterrows():
    article = MyNews(
        ticker=row['Ticker'],
        date=row['Date'],
        time=row['Time'],
        headline=row['Headlines'],
        sentiment=row['compound']
    )
    sesh.add(article)
sesh.commit()


# Grouping by date and ticker
# sentiment_trend = data_frame.groupby(['Date', 'Ticker'])['compound'].mean().unstack()

#-----------------------------------------------------------
# Visualization Of Sentiment Analysis
#-----------------------------------------------------------

#-----------------------------------------------------------
# Bar Chart
# plt.close('all')  # Closing any existing figure windows

# sentiment_trend.plot(kind='bar', figsize=(11, 7))

# plt.title('Sentiment Trend Over Time')
# plt.xlabel('Date')
# plt.ylabel('Average Sentiment Score')
# plt.legend(title='Ticker')
# plt.grid(True)
# plt.show()
#-----------------------------------------------------------

# Trend Line
#-----------------------------------------------------------
# plt.figure(figsize=(11, 5))

# for ticker in ticker_symbols:
#     plt.plot(sentiment_trend.index, sentiment_trend[ticker], label=ticker)

# plt.title('Sentiment Trend Over Time')
# plt.xlabel('Date')
# plt.ylabel('Average Sentiment Score')
# plt.legend(title='Ticker')
# plt.grid(True)
# plt.show()
#-----------------------------------------------------------

