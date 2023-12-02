import backtrader as bt
from strategies import RandomStrategy
import pytest

class TestStrategies:

    def _common_procedure(self, class_name):
        cerebro = bt.Cerebro()
        cerebro.addstrategy(class_name)
        data = bt.feeds.YahooFinanceCSVData(dataname='./test/data/ACA.PA.csv')
        cerebro.adddata(data)
        cerebro.broker.setcash(100000.0)
        cerebro.run()
        return cerebro.broker.getvalue()

    def test_RandomStrategy(self):
        final_value = self._common_procedure(RandomStrategy.RandomStrategy)
        assert(final_value == pytest.approx(100212.81, abs=0.01))
