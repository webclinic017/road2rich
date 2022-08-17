import backtrader as bt


class GridStrategy(bt.Strategy):
    params = (
        ('exitbars',5),
        ('maperiod',15),
        ('grid_size',0.10),
        ('order_size',100)
    )

    def __init__(self) -> None:
        '''
            最基本的网格策略：
                1、手上资金量为25手（即25*100*当前价格）
                2、初期按照当前价格买入10手
                3、每当价格价格相当于上一次交易：
                    3.1 高出10%时，卖出1手
                    3.2 低于10%时，买入一手
                4、限制：
                    4.1 卖光为止；
                    4.2 最多买入20手；
        '''
        self.dataclose = self.datas[0].close
        self.order = None
        self.last_trade_price = None
        
        
    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        dt = self.datas[0].datetime.date(0).isoformat()

        if dt<='2017-01-01':
            return

        
        if self.last_trade_price is None:
            self.buy(size=10*self.params.order_size)
        else:
            if self.dataclose[0]>(1+self.params.grid_size)*self.last_trade_price:
                if self.position:
                    self.sell(size=self.params.order_size)
            elif self.dataclose[0]<(1-self.params.grid_size)*self.last_trade_price:
                if self.position.size<20*self.params.order_size:
                    self.buy(size=self.params.order_size)
            
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
            self.last_trade_price = order.executed.price

            # 记录当前交易数量
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金不足/拒绝')

        # 其他状态记录为：无挂起订单
        self.order = None
    
