from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

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
    news_table = html_output.find(id="news-table")
    news_tables[ticker] = news_tables

    # print(html_output)
    # print(response)
    break

print(news_tables['AMZN'])

