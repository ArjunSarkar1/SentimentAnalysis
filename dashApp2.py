import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from sqlalchemy import create_engine

# Load data from the database
engine = create_engine('sqlite:///my_news.db')
df = pd.read_sql('News_Headlines', engine)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=df['date'].min(),
        end_date=df['date'].max(),
        display_format='YYYY-MM-DD'
    ),
    dcc.Graph(id='sentiment-graph'),
    dcc.Graph(id='bar-chart')
])

@app.callback(
    [Output('sentiment-graph', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(start_date, end_date):
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    filtered_df = df[mask]

    sentiment_trend = filtered_df.groupby(['Date', 'Ticker'])['compound'].mean().unstack()

    line_fig = {
        'data': [
            {'x': sentiment_trend.index, 'y': sentiment_trend[ticker], 'type': 'line', 'name': ticker}
            for ticker in sentiment_trend.columns
        ],
        'layout': {
            'title': 'Sentiment Trend Over Time'
        }
    }

    bar_fig = {
        'data': [
            {'x': sentiment_trend.index, 'y': sentiment_trend[ticker], 'type': 'bar', 'name': ticker}
            for ticker in sentiment_trend.columns
        ],
        'layout': {
            'title': 'Sentiment Distribution'
        }
    }

    return line_fig, bar_fig

if __name__ == '__main__':
    app.run_server(debug=True)
