import backtrader as bt
import random

class RandomStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        random.seed(42)

    def next(self):
        # Simply log the closing price of the series from the reference
        choice = random.randint(1, 3)
        if choice == 1:
            self.buy()
        elif choice == 2:
            self.sell()
