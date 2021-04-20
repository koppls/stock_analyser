# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 15:56:14 2020

Unit-test for Stock_Analyser program

@author: VT_SA
"""

import unittest
import pandas as pd
import numpy as np
import yfinance as yf
from scipy import stats
from prediction import predict_value, predict_series
from data import get_data

ticker_str = "AAPL"
start_date = "2019-11-23"
end_date = "2020-11-23"
intvl = "1d"
ticker = yf.Ticker(ticker_str)

stock_data = ticker.history(start = start_date, end = end_date, interval = intvl)
num_data_points = len(stock_data["Close"])
days = np.arange(num_data_points)
lr = stats.linregress(days, stock_data['Close'])
trendline = lr.intercept + lr.slope * days

class StockAnalyserTest(unittest.TestCase):

    def test_prediction_value(self):
        """ tests function if it calculates 1 prediction value
        in n days correctly """
        # given the above static data, Excel calculated those values:
        # 57.387372836332 + 0.251764995965033 * (251 + 5) = 121.84
        # 57.387372836332 + 0.251764995965033 * (251 + 10) = 123.1
        self.assertEqual(round(predict_value(lr, num_data_points, 5),2), 121.84)
        self.assertEqual(round(predict_value(lr, num_data_points, 10),2), 123.1)

    def test_prediction_valuepredict_series(self):
        """ tests function if it calculates the list of
        prediction values from End Date to n days correctly """
        # Excel: 57.387372836332 + 0.251764995965033 * (251 + 1), [...] * (251 + 2)...
        # -> 120.83	121.08	121.34	121.59	121.84	122.09	122.34	122.59	122.85	123.1
        self.assertEqual(predict_series(lr, num_data_points, 5), [120.83, 121.08, 121.34, 121.59, 121.84])
        self.assertEqual(predict_series(lr, num_data_points, 10),
                        [120.83, 121.08, 121.34, 121.59, 121.84, 122.09, 122.34, 122.59, 122.85, 123.1])

    def test_get_data(self):
        """ tests function if it adds columns to dateframe correctly """
        # https://stackoverflow.com/questions/47019730/apply-asserttrue-unit-testing-to-pandas-dataframe
        # call function and return updated dataframe
        stock_data_upd = get_data(ticker, ticker_str, start_date, end_date)
        # check if 4 additional cols have been added correctly
        self.assertTrue("Short Term MA (50d)" in stock_data_upd)
        self.assertTrue("Long Term MA (200d)" in stock_data_upd)
        self.assertTrue("MACD" in stock_data_upd)
        self.assertTrue("MACD Signal" in stock_data_upd)

if __name__ == '__main__':
    unittest.main()
