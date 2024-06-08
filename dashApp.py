import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from main import sentiment_trend

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Stock Sentiment Analysis"),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in sentiment_trend.columns],
        value=sentiment_trend.columns[0],
        multi=True
    ),
    dcc.Graph(id='sentiment-graph')
])

# Callback to update the graph
@app.callback(
    Output('sentiment-graph', 'figure'),
    [Input('ticker-dropdown', 'value')]
)
def update_graph(selected_tickers):
    if not selected_tickers:
        return px.line()
    
    fig = px.line(sentiment_trend[selected_tickers].reset_index(), x='Date', y=selected_tickers)
    fig.update_layout(title='Sentiment Trend Over Time', xaxis_title='Date', yaxis_title='Average Sentiment Score')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
