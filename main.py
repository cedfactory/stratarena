from strategies import RandomStrategy
import backtrader as bt

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(RandomStrategy.RandomStrategy)

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(dataname='./ACA.PA.csv')

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    figure = cerebro.plot()[0][0]
    figure.savefig('example.png')
