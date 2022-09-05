import pandas as pd
import pandas_datareader as web
from datetime import datetime
import plotly.graph_objs as go
import plotly


#start = datetime(2021, 9, 8)
#end = datetime(2020, 7, 31)
#stock = 'TSLA'


#df = web.DataReader(stock, 'yahoo', start)
#df = df.reset_index()
#print(df)

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
    create_chart(pd.read_csv('AMZN.csv'))


#plotly.offline.plot(fig, filename='Candlestick.html')
