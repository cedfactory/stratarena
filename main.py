# https://www.youtube.com/watch?v=JOdEZMcvyac&t=438s
# https://vectorbt.dev/api/indicators/basic/#vectorbt.indicators.basic.RSI.rsi_crossed_above
# portfolio metrics:
# https://vectorbt.dev/api/portfolio/base/#vectorbt.portfolio.base.Portfolio.metrics
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import vectorbt as vbt


def section_1(price):
    print(price)
    print(type(price))
    rsi = vbt.RSI.run(price, window=[14])
    print(rsi.rsi)
    entries = rsi.rsi_crossed_below(30)
    # print(entries.to_string())
    exits = rsi.rsi_crossed_above(70)
    # print(exits.to_string())
    pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=10000)
    pf.plot().show()
    # print(pf.total_return())
    # print(pf.total_profit())
    # print(pf.stats())


def custom_indicator(close, rsi_window=14, ma_window=50, entry=30, exit=70):
    close_5m = close.resample("5T").last()
    # rsi = vbt.RSI.run(close, window=rsi_window).rsi.to_numpy()
    rsi = vbt.RSI.run(close_5m, window=rsi_window).rsi
    rsi, _ = rsi.align(close,
                       broadcast_axis=0,
                       method='ffill',
                       join='right')
    #rsi = rsi.ffill() ?

    close = close.to_numpy()
    rsi = rsi.to_numpy()
    ma = vbt.MA.run(close, window=ma_window).ma.to_numpy()

    trend = np.where(rsi > exit, -1, 0)
    trend = np.where((rsi < entry) & (close < ma), 1, trend)

    return trend

def section_2(prices):
    ind = vbt.IndicatorFactory(
        class_name="Combination",
        short_name='comb',
        input_names=['close'],
        param_names=['rsi_window', "ma_window", "entry", "exit"],
        output_names=['value']
    ).from_apply_func(
        custom_indicator,
        rsi_window=14,
        ma_window=100,
        entry=30,
        exit=70,
        keep_pd=True
    )
    res = ind.run(prices,
                  # rsi_window=[14, 35, 21],
                  rsi_window=np.arange(10, 40, step=3, dtype=int),
                  # ma_window=[21, 50, 100],
                  # ma_window=np.arange(20, 200, step=20, dtype=int),
                  # entry=[30, 40],
                  entry=np.arange(10, 40, step=4, dtype=int),
                  # exit=[60, 70],
                  exit=np.arange(60, 90, step=4, dtype=int),
                  param_product=True
                  )

    # print(res.value.to_string())
    # print(res.value)

    entries = res.value == 1
    exits = res.value == -1

    pf = vbt.Portfolio.from_signals(prices, entries, exits, init_cash=10000)

    # print(pf.stats())
    print(pf.total_return().to_string())
    print(pf.total_profit().to_string())

    returns = pf.total_return()
    profits = pf.total_profit()
    print(returns.max())
    print(returns.idxmax())
    print(profits.max())
    print(profits.idxmax())

    returns = pf.total_return()
    profits = pf.total_profit()


def get_prices(lst_pairs):
    # Prepare data
    interval = "1m" # \in { "1h", "1m" }
    #end = datetime.utcnow().strftime("%Y-%m-%d %Z %H:%M")
    end_date = datetime.now()
    if interval == "1h":
        start_date = end_date - timedelta(days=15)
    else:
        start_date = end_date - timedelta(days=7) #"2023-01-01 00:00"

    prices = vbt.YFData.download(lst_pairs, interval=interval, start=start_date, end=end_date, missing_index='drop').get('Close')
    #print(prices)
    return prices


if __name__ == '__main__':

    print("section_1")
    prices = get_prices(['BTC-USD'])
    section_1(prices)

    print("section_2")
    lst_pairs = ['BTC-USD', 'ETH-USD'] # ['BTC-USD', 'ETH-USD', 'XRP-USD', 'ADA-USD']
    prices = get_prices(lst_pairs)
    section_2(prices)
