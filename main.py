# https://www.youtube.com/watch?v=JOdEZMcvyac&t=438s
# https://vectorbt.dev/api/indicators/basic/#vectorbt.indicators.basic.RSI.rsi_crossed_above
# portfolio metrics:
# https://vectorbt.dev/api/portfolio/base/#vectorbt.portfolio.base.Portfolio.metrics
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import vectorbt as vbt

def custom_indicator(close, rsi_window=14, ma_window=50, entry=30, exit=70):
    close_5m = close.resample("5T").last()
    # rsi = vbt.RSI.run(close, window=rsi_window).rsi.to_numpy()
    rsi = vbt.RSI.run(close_5m, window=rsi_window).rsi
    rsi, _ = rsi.align(close,
                       broadcast_axis=0,
                       method='ffill',
                       join='right')
    close = close.to_numpy()
    rsi = rsi.to_numpy()
    ma = vbt.MA.run(close, window=ma_window).ma.to_numpy()

    trend = np.where(rsi > exit, -1, 0)
    trend = np.where((rsi < entry) & (close < ma), 1, trend)

    return trend

if __name__ == '__main__':
    """
    data = vbt.BinanceData.fetch(
        ["BTCUSDT"],
        start="2019-01-01 UTC",
        end="2023-02-02 UTC",
        timeframe="1m"
    )
    """

    # Prepare data
    end = datetime.utcnow().strftime("%Y-%m-%d %Z %H:%M")
    end_date = datetime.now()
    # start = '2023-01-01 UTC'  # crypto is in UTC
    start = '2023-01-01 00:00'  # crypto is in UTC
    start_date_1m = end_date - timedelta(days=3) # For interval 1m
    start_date_1h = '2023-01-01 00:00'  # crypto is in UTC

    # btc_price = vbt.YFData.download('BTC-USD', start=start, end=end, missing_index='drop').get('Close')
    # eth_price = vbt.YFData.download('ETH-USD', start=start, end=end, missing_index='drop').get('Close')

    # interval = "1h"
    interval = "1m"
    lst_pairs = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'ADA-USD']
    # lst_pairs = ['BTC-USD']
    lst_pairs = ['BTC-USD', 'ETH-USD']
    if interval == "1m":
        btc_price = vbt.YFData.download(lst_pairs,
                                        interval="1m",
                                        start=start_date_1m,
                                        end=end_date,
                                        missing_index='drop').get('Close')
        print(btc_price)
    else:
        # btc_price = vbt.YFData.download(['BTC-USD', 'ETH-USD', 'XRP-USD', 'ADA-USD'],
        btc_price = vbt.YFData.download(lst_pairs,
                                        interval="1h",
                                        start=start_date_1h,
                                        end=end_date,
                                        missing_index='drop').get('Close')
    section = "section_1"
    #section = "section_2"

    if section == "section_1":
        print(btc_price)
        print(type(btc_price))
        rsi = vbt.RSI.run(btc_price, window=[14])
        print(rsi.rsi)
        entries = rsi.rsi_crossed_below(30)
        # print(entries.to_string())
        exits = rsi.rsi_crossed_above(70)
        # print(exits.to_string())
        pf = vbt.Portfolio.from_signals(btc_price, entries, exits, init_cash=10000)
        pf.plot().show()
        # print(pf.total_return())
        # print(pf.total_profit())
        # print(pf.stats())

