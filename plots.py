# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 21:02:05 2020

Class for graphs/ plots

@author: Sabine Kopplin
"""

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from prediction import linear_reg, predict_value, predict_series

class Graphs:
    """ class to define graphs """

    def __init__(self, stock_data, ticker_str, company_name):
        self.stock_data = stock_data
        self.ticker_str = ticker_str
        self.company_name = company_name
        sns.set(style="darkgrid")

    def timeseries(self):
        """ generate plot of Closing Price and Volume """

        plt.figure(num="Time Series - Price & Volume");
        # https://subscription.packtpub.com/book/big_data_and_business_intelligence/9781787123137/15/ch15lvl1sec125/plotting-volume-series-data
        # plot closing price in graph (top)
        top = plt.subplot2grid((5,4), (0,0),rowspan=3,colspan=4)
        top.plot(self.stock_data["Close"].index, self.stock_data["Close"], label="Closing Price", color="#154892")
        plt.title("{}'s ({}) Closing Price".format(self.company_name,self.ticker_str, size=14))
        plt.ylabel("Share Price in $", size=12)

        # plot trade volume in graph (bottom)
        bottom = plt.subplot2grid((5,4), (3,0),rowspan=2,colspan=4)
        bottom.bar(self.stock_data.index, self.stock_data["Volume"], width=1, color="#154892", edgecolor="#154892")
        plt.title("{}'s ({}) Trading Volume".format(self.company_name, self.ticker_str, size=14))
        plt.ylabel("Vol per 1eN ", size=12)

        plt.subplots_adjust(hspace=0.75)
        plt.gcf().set_size_inches(15,14)
        # show graph
        Graphs.max_graph()
        plt.show()

    def timeseries_trend(self, trendline):
        """ generate plot of Closing Price including trend line (linear regression) """

        plt.figure(num="Time Series with Linear Trend");
        # make graph look pretty
        Graphs.graph_layout()
        # plot in a graph
        plt.plot(self.stock_data.index, trendline, color="#8FA8CC", label="Linear Trend", linestyle='dashed', alpha=0.8)
        self.stock_data["Close"].plot(label="Closing Price", color="#154892")
        plt.title("{}'s ({}) Closing Price incl. Linear Trend".format(self.company_name, self.ticker_str, size=14))
        plt.legend(loc='upper left',facecolor="white")
        # show graph
        Graphs.max_graph()
        plt.show()

    def ma_compare(self):
        """ generate plot of Short Term and Long Term Moving Average (MA) """

        plt.figure(num="Moving Average Cross");
        # make graph look pretty
        Graphs.graph_layout()
        # plot in a graph
        self.stock_data["Short Term MA (50d)"].plot(label="Short Term MA (50d)", color="#8FA8CC")
        self.stock_data["Long Term MA (200d)"].plot(label="Long Term MA (200d)", color="#154892")
        plt.title("{}'s ({}) Moving Average Cross".format(self.company_name, self.ticker_str, size=14))
        plt.legend(loc='upper left',facecolor="white")
        # show graph
        Graphs.max_graph()
        plt.show()

    def wma_vs_close(self):
        """ generate plot of weighted Moving Average (MA) and Closing Price """

        plt.figure(num="Weighted MA vs Closing Price");
        # make graph look pretty
        Graphs.graph_layout()
        # plot in a graph
        self.stock_data["Close"].plot(label="Closing Price", color="#4C6FA1",
                                      alpha=0.8, linestyle='dashed', linewidth=0.9)
        self.stock_data["Weighted MA (10d)"].plot(label="Weighted MA (10d)", color="#154892")
        plt.title("{}'s ({}) Weighted Moving Average vs Closing Price".format(self.company_name,
                                                                              self.ticker_str,
                                                                              size=14))
        plt.legend(loc='upper left', facecolor="white")
        # show graph
        Graphs.max_graph()
        plt.show()

    def macd(self):
        """ generate plot of MACD - Relationship between EMA of 12 days vs 26 days  """

        plt.figure(num="MACD");
        # create baseline at 0
        baseline = np.zeros(len(self.stock_data["Close"]))
        # plot in a graph
        plt.plot(self.stock_data.index, baseline, color="#8FA8CC",
                 label="Baseline", linestyle='dashed', alpha=0.8)
        self.stock_data["MACD Signal"].plot(label="Signal Line", color="#F0A755")
        self.stock_data["MACD"].plot(label="MACD", color="#154892")
        # make graph look pretty
        plt.title("{}'s ({}) MACD".format(self.company_name, self.ticker_str, size=14))
        plt.legend(loc='upper left', facecolor="white")
        plt.ylabel("")
        plt.xlabel("")
        # show graph
        Graphs.max_graph()
        plt.show()

    def graph_layout():
        # define graph layout and plot
        plt.ylabel("Closing Price in $", size=12)
        plt.xlabel("")
        plt.xticks(size=11)
        plt.yticks(size=11)

    def max_graph():
        # https://stackoverflow.com/questions/12439588/how-to-maximize-a-plt-show-window-using-python
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
