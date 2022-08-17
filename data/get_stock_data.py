from pickle import FALSE
import akshare as ak
from datetime import datetime
import glob
import pandas as pd
import os


LOCAL_PATH = os.path.split(os.path.realpath(__file__))[0]
DATA_PATH = os.path.join(LOCAL_PATH,'stock')

def download_stock_data(stock_code,start_date,end_date):
    """_summary_

    Args:
        stock_code (_type_): _description_
        start_date (_type_): _description_
        end_date (_type_): _description_

    Returns:
        _type_: _description_
    """

    # stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20170301", end_date='20210907', adjust="")
    
    df = ak.stock_zh_a_hist(symbol=stock_code,period='daily',
                            start_date=start_date,
                            end_date=end_date)
    return df

def get_stock(stock_code,start_date,end_date):
    loaded_code = {file_name.split('/')[-1].split('_')[0]:file_name for file_name in glob.glob(os.path.join(DATA_PATH,'*.csv'))}
    potential_name = f"{stock_code}_{start_date}_{end_date}.csv"
    if stock_code not in loaded_code:
        # 没有直接下载
        print(f'DOWNLOAD {stock_code}')
        df = download_stock_data(stock_code,start_date,end_date)
        saving_name = os.path.join(DATA_PATH,potential_name)
        df.to_csv(saving_name,index=False)
    else:
        file_name = loaded_code[stock_code].split('/')[-1].split('.')[0]
        if file_name == potential_name:
            # 有且时间一致就直接用
            print(f"LOAD {stock_code}")
            df = pd.read_csv(loaded_code[stock_code])
        else:
            # 有但时间不一致，那么就下载-merge-去重返回
            old_df = pd.read_csv(loaded_code[stock_code])
            new_df = download_stock_data(stock_code,start_date,end_date)
            merge_df = pd.concat([old_df,new_df]).drop_duplicates().sort_values(by='日期')
            merge_start_date = merge_df.iloc[0]['日期'].replace('-','')
            merge_end_date = merge_df.iloc[-1]['日期'].replace('-','')
            merge_df.to_csv(os.path.join(DATA_PATH,f"{stock_code}_{merge_start_date}_{merge_end_date}.csv"),index=False)
            print(f"LOAD {stock_code} and merge to {merge_start_date} and {merge_end_date}")

            df = merge_df

    return df



if __name__ == '__main__':
    from tqdm import tqdm
    index_stock_cons_csindex_df = ak.index_stock_cons_csindex(symbol="399986")
    print(index_stock_cons_csindex_df.head())
    
    for _,row in tqdm(index_stock_cons_csindex_df.iterrows()):
        code = row['成分券代码']
        get_stock(code,start_date='20150517',end_date='20220811')