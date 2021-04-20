# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:51:41 2020

Functions to predict values based on linear regression

@author: Sabine Kopplin
"""
import numpy as np
from scipy import stats
import tkinter.messagebox as msg
from sklearn.metrics import mean_squared_error as mse

def linear_reg(stock_data):
    """ Linear Regression """
    # compute days in the index
    num_data_points = len(stock_data["Close"])
    days = np.arange(num_data_points)

    # code based on code of slide 39, lecture 7a "Pandas"
    # calculate trendline with linear regression
    lr = stats.linregress(days, stock_data['Close'])
    trendline = lr.intercept + lr.slope * days
    rmse = round(mse(stock_data["Close"], trendline, squared=False),5)
    return num_data_points, lr, trendline, rmse

def predict_value(lr, num_data_points, daysinfuture):
    """ predict closing price in n days """
    pred_val = lr.intercept + lr.slope * (num_data_points + daysinfuture)
    return round(pred_val,2)

def predict_series(lr, num_data_points, daysinfuture):
    """ predict all closing prices from end date to n days """
    pred_list = []
    for i in range(num_data_points + 1, num_data_points + 1 + daysinfuture):
        pred_list.append(round((lr.intercept + lr.slope * i),2))
    return pred_list
