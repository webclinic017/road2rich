from audioop import reverse
import os
import backtrader as bt
import datetime
from mystrategy.test import TestStrategy
from mystrategy.grid import GridStrategy

FILE_PATH = os.path.split(os.path.realpath(__file__))[0]


if __name__ == '__main__':

    cerebro = bt.Cerebro()

    # 1、add data
    # datapath = './data/orcl-1995-2014.txt'
    # data = bt.feeds.YahooFinanceCSVData(
    #     dataname=datapath,
    #     # 数据必须大于fromdate
    #     fromdate=datetime.datetime(2000, 1, 1),
    #     # 数据必须小于todate
    #     todate=datetime.datetime(2000, 12, 31),
    #     reverse=False)
    data = bt.feeds.GenericCSVData(
        # dataname='data/index/sz159949_updaet_at_20220813.csv',
        dataname='data/stock/601166_20150517_20220811.csv',
        fromdate = datetime.datetime(2016,1,1), # 20160722
        todate = datetime.datetime(2017,12,31), # 20220814
        reverse=False,
        dtformat=('%Y-%m-%d'),
        datetime=0,
        high=2,
        low=3,
        open=1,
        close=4,
        volume=5,
        openinterest=-1
    )

    cerebro.adddata(data)

    # 2、add strategy
    # cerebro.addstrategy(TestStrategy)
    cerebro.addstrategy(GridStrategy)

    # 3、add cash
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)

    # 4、set size
    cerebro.addsizer(bt.sizers.FixedSize, stake=1000) 

    # 5、add analysers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown,_name='mydrwadown')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='myannual')



    # 6、run
    print(f"start {cerebro.broker.getvalue()}")
    thestrats = cerebro.run()
    thestrat = thestrats[0]    
    print(f"final {cerebro.broker.getvalue()}")

    # 5、plot
    # cerebro.plot()
    print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
    print('DrawDown',thestrat.analyzers.mydrwadown.get_analysis())
    print('AnnualReturn',thestrat.analyzers.myannual.get_analysis())



    





