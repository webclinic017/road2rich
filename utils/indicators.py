import pandas as pd


def get_volatility(df):
    return abs(df['close']-df['open'])/df['open']
