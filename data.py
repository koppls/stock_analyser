# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 14:42:31 2020

Data Gathering
- Functions for storing data via API in dataframe & preparing descriptive analysis

@author: Sabine Kopplin
"""

import pandas as pd
import numpy as np
import yfinance as yf
from scipy import stats
from sklearn.metrics import mean_squared_error as mse
import tkinter.messagebox as msg

def get_data(ticker, ticker_str, start_date, end_date):
    """ get data from user input in GUI and return dateframe with
        all stock data necessary for further analysis """
    # https://towardsdatascience.com/a-comprehensive-guide-to-downloading-stock-prices-in-python-2cd93ff821d4
    # get stock data from yfinance via API and store in dateframe
    stock_data = ticker.history(ticker_str, start= start_date,
                                end=end_date, interval="1d")
    # https://towardsdatascience.com/moving-average-technical-analysis-with-python-2e77633929cb
    # add new columns in stock_data df for simple moving averages
    # short term: 50 days | long term: 200 days
    stock_data["Short Term MA (50d)"] = stock_data["Close"].rolling(50).mean()
    stock_data["Long Term MA (200d)"] = stock_data["Close"].rolling(200).mean()
    # https://towardsdatascience.com/trading-toolbox-02-wma-ema-62c22205e2a9
    # create array of weights for simple weighted moving average
    weights = np.arange(1,11)
    # add new column in stock_data df for weighted moving average of 10 days
    stock_data["Weighted MA (10d)"] = stock_data["Close"].rolling(10).apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)
    # calculate exponential moving average for 12 and 26 days
    ema12 = round(stock_data["Close"].ewm(span=12).mean(),3)
    ema26 = round(stock_data["Close"].ewm(span=26).mean(),3)
    # add new column in stock_data df for MACD
    stock_data["MACD"] = ema12 - ema26
    # add new column in stock_data df for MACD Signal
    stock_data["MACD Signal"] = round(stock_data["MACD"].ewm(span=9).mean(),3)

    return stock_data

def descriptive_stats(stock_data, ticker_str, ticker):
    """ print all descriptive data and stats on command line """

    msg.showinfo("Notice", "The data will be printed on the command line.")
    # print Stock Data Overview
    print("")
    print("*"*100)
    print("")
    print("{} DATA SUMMARY".format(ticker.info["shortName"].upper()))
    print("")
    print("-"*100)
    # print first 5 rows of data table
    print("Data Head:\n{}".format(stock_data.head()))
    print("")
    print("-"*100)
    # print last 5 rows of data table
    print("Data Tail:\n{}".format(stock_data.tail()))
    print("")
    print("-"*100)
    print("")
    # print descriptive statistics based on user input
    calc_descriptive(stock_data)
    print("")
    # create table for pretty output and print on command line
    row = "| {:16} | {:12} |"
    print("{:=^35}".format(" " + ticker_str + " Overview "))
    # print general stock information based on yfinance data
    print(row.format("52-week Low", ticker.info["fiftyTwoWeekLow"]))
    print(row.format("52-week High:", ticker.info["fiftyTwoWeekHigh"]))
    print(row.format("52-week Avg.", round(ticker.info["fiftyDayAverage"],2)))
    print(row.format("PREVIOUS CLOSE:", ticker.info["previousClose"]))
    print(row.format("Trailing PE:", round(ticker.info["trailingPE"],2)))
    print("=" * 35)
    print("")
    print("*"*100)

def calc_descriptive(stock_data):
    """calculate descriptive data based on
        closing price and time range as per user input """
   # calculate various descriptive statistics
    mean = round(stock_data["Close"].mean(),2)
    std = round(stock_data["Close"].std(),2)
    max_val = round(stock_data["Close"].max(),2)
    min_val = round(stock_data["Close"].min(),2)
    range_max_min = round(max_val - min_val,2)
    cov = round((std/mean),2)*100
    q1 = round(stock_data["Close"].quantile(0.25),2)
    q2 = round(stock_data["Close"].quantile(0.5),2)
    q3 = round(stock_data["Close"].quantile(0.75),2)

    # create table for pretty output and print on command line
    row = "| {:16} | {:12} |"
    print("{:=^35}".format(" Closing Price Summary "))
    print(row.format("\u03BC (mean)", mean))
    print(row.format("\u03C3 (std)", std))
    print(row.format("COV", cov))
    print(row.format("Min", min_val))
    print(row.format("Q1 (25%)", q1))
    print(row.format("Q2 (50%)", q2))
    print(row.format("Q3 (75%)", q3))
    print(row.format("Max", max_val))
    print(row.format("Range", range_max_min))
    print("=" * 35)
