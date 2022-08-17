import akshare as ak
from datetime import datetime
import glob
import pandas as pd
import os


LOCAL_PATH = os.path.split(os.path.realpath(__file__))[0]
DATA_PATH = os.path.join(LOCAL_PATH,'index')
# print(local_path)

def download_stockindex_history(stock_code,saving_name=None,):
    """_summary_
    下载指数数据
    Args:
        stock_code (_type_): _description_. sh000300,sh000001
        saving_name (_type_, optional): _description_. Defaults to None.
    """
    if saving_name is None:
        now_day = datetime.now().strftime("%Y%m%d")
        saving_name = os.path.join(DATA_PATH,f"{stock_code}_updaet_at_{now_day}.csv")
    
    df = ak.stock_zh_index_daily(symbol=stock_code)
    df.to_csv(saving_name)
    return df

def get_stockindex(stock_code):
    """从本地或者网上拿到其记录的，对应指数的，全量历史数据

    Args:
        stock_code (_type_): _description_

    Returns:
        _type_: _description_
    """
    loaded_index = {file_name.split('/')[-1].split('_')[0] :file_name for file_name in glob.glob(os.path.join(DATA_PATH,'*.csv'))}
    # print(loaded_index)
    if stock_code in loaded_index:
        print(f"Load {stock_code} from Disk.")
        return pd.read_csv(loaded_index[stock_code])
    else:
        print(f"Download {stock_code}.")
        return download_stockindex_history(stock_code)

def get_stockindex_realtime():
    stock_zh_index_spot_df = ak.stock_zh_index_spot()
    stock_zh_index_spot_df.to_csv(os.path.join(DATA_PATH,'all_stockindex_realtime.csv'),index=False)
    print("GET ALL STOCKINDEX REALTIME DATA")

    return stock_zh_index_spot_df

    
if __name__ == '__main__':
    df_000300 = get_stockindex('sz159949') #sh000300,sz399986
    # # get_stockindex_realtime()
    # index_stock_cons_csindex_df = ak.index_stock_cons_csindex(symbol="399986")

    # print(index_stock_cons_csindex_df)
    





