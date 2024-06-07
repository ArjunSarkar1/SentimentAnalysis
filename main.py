from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# NLTK
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas

finviz_url = "https://finviz.com/quote.ashx?t="
ticker_symbols = ['AMZN','AMD','FB', 'AAPL']

news_tables = {} 

for ticker in ticker_symbols:
    url = finviz_url + ticker

    # making a request to acquire html data from the
    # above urls
    req = Request(url=url, headers={'user-agent': 'test-app'})
    response = urlopen(req)
    
    html_output = BeautifulSoup(response, features='html.parser')
    tables = html_output.find(id="news-table")
    news_tables[ticker] = tables

    # print(html_output)
    # print(response)
    break

"""
Parsed Data List consists of:
- Ticker Symbol
- Date
- Time
- News HeadLine 
"""
all_parsed_data = []
all_parsed_data_links = []

for ticker, news in news_tables.items():

    for rows in tables.findAll('tr'):
        headlines = rows.a.text.strip()
        date_time = rows.td.text.strip().split(' ')
        headline_link = rows.findAll('td')[1].a['href']

        if len(date_time) > 1:
            date = date_time[0]
            time = date_time[1]
        else:
            time = date_time[0]

        all_parsed_data.append([ticker, date, time, headlines])
        all_parsed_data_links.append([headline_link])

data_frame = pandas.DataFrame(all_parsed_data, columns=['Ticker','Date','Time','Headlines'])
vader = SentimentIntensityAnalyzer()

function = lambda headlines: vader.polarity_scores(headlines)['compound']
data_frame['compound'] = data_frame['Headlines'].apply(func = function)

print(data_frame.head())
# print(data_frame)

# for row in amzn_data.findAll('tr'):
#     print(row.td.text.strip() + " -> " + row.a.text.strip())    
#     print("-" * 80)
# print(f"Link: {link}")
# print(f"Date & Time: {date_time}")
# print(f"Headline: {headlines}")
# print(f"Link: {link}")

