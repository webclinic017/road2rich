import backtrader as bt


class TestStrategy(bt.Strategy):
    params = (
        ('exitbars',5),
        ('maperiod',15),
    )

    def __init__(self) -> None:
        self.dataclose = self.datas[0].close
        self.order = None
        # 是否有这个的不同：
        #   会在sma产生第一个数据后才开始计算策略
        #   所以有无sma的结果是不同的
        # self.sma = bt.indicators.MovingAverageSimple(self.datas[0],period=self.params.maperiod)
    
    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if not self.position:
            if self.dataclose[0]<self.dataclose[-1]<self.dataclose[-2]:
                self.log('买入, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            # 如果已经持仓，且当前交易数据量在买入后5个单位后
            if len(self) >= (self.bar_executed + self.params.exitbars):
                # 全部卖出
                self.log('卖出, %.2f' % self.dataclose[0])
                # 跟踪订单避免重复
                self.order = self.sell()

    
    def log(self, txt, dt=None):
        # 记录策略的执行日志
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    

    def notify_order(self, order):
        """处理订单的回调函数

        Args:
            order (_type_): _description_
        """
        if order.status in [order.Submitted, order.Accepted]:
            # broker 提交/接受了，买/卖订单则什么都不做
            return

        # 检查一个订单是否完成
        # 注意: 当资金不足时，broker会拒绝订单
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('已买入, %.2f' % order.executed.price)
            elif order.issell():
                self.log('已卖出, %.2f' % order.executed.price)

            # 记录当前交易数量
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金不足/拒绝')

        # 其他状态记录为：无挂起订单
        self.order = None
    
    def notify_trade(self, trade):
        self.log(f"trade: {trade.status} {trade.price} {trade.size}")
        
        # return super().notify_trade(trade)