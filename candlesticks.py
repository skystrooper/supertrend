import pandas as pd
import plotly.graph_objs as go

def create_chart(df):
    fig = go.Figure(data=[go.Candlestick(
                                x=df['Date'],
                                open=df['Open'],
                                high=df['High'],
                                low=df['Low'],
                                close=df['Adj Close']
                                )])

    fig.show()

if __name__ == '__main__':
    create_chart(pd.read_csv('stockdata.csv'))
