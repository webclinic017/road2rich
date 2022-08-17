from tokenize import PlainToken
import pandas as pd
import matplotlib.pyplot as plt


def cut2Align(df_list,align_col='date'):
    start_date = max([a.iloc[0][align_col] for a in df_list])
    end_date = min([a.iloc[-1][align_col] for a in df_list]) 
    ret_list = []
    for df in df_list:
        ret_list.append(df[(df[align_col]>=start_date) & (df[align_col]<=end_date)])
    return ret_list

if __name__ == '__main__':
    pass
