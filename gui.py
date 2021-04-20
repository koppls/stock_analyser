# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 12:01:05 2020

User Interface
- Class for main window with menu
- Class for GUI tools (e.g. buttons, labels...)

@author: Sabine Kopplin
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar,DateEntry
import tkinter.messagebox as msg
import datetime
import yfinance as yf
from data import get_data, descriptive_stats
from plots import Graphs
from prediction import linear_reg, predict_value, predict_series
from datetime import timedelta

# Code from Lecture 8b "Event-driven Programming"
class StockAnalyser_Main:
    """ create GUI for data input and analytics selection """

    getdata_button_clicked = False

    def __init__(self, master):
        # Save master reference
        self.master = master
        # Set window title
        master.title("Stock Analyser")
        self.master.configure(background="#5991CA")

        # Create a welcome label
        Gui_Tools.create_header(self.master, "Welcome, let's analyse a stock.", 14)

        # Create entry box for stock ticker
        self.stocktkr_entry = Gui_Tools.create_entrybox(self.master,
                                "Enter a Stock Ticker:", 1, 0)

        # Create a time series selection label
        Gui_Tools.create_header(self.master, "Select a Time Series to analyse:", 11)

        # Create calendar for start date for Time Series
        self.startdate = Gui_Tools.create_dateentry(self.master,
                                                    "Start Date", 2010, 3, 0)
        # Create calendar for end date for Time Series
        self.enddate = Gui_Tools.create_dateentry(self.master,
                                                  "End Date", 2020, 4, 0)

        # Create entry box for prediction day(s)
        Gui_Tools.create_header(self.master, "Predict the future:", 11)
        self.daysinfuture_entry = Gui_Tools.create_entrybox(self.master,
                                    "Enter a day (0-20):", 6, 0)

        # Create OK button to get data from input fields
        Gui_Tools.create_button(master, "OK", "SystemButtonFace", "black", self.get_input)

        # create 2 combobox for descriptive + predictive analytics events
        self.str_descr_selected, self.select_descriptive = Gui_Tools.create_combobox(self.master,
                                                            "Select the Descriptive Analytics: ",
                                                            self.descriptive)
        self.str_pred_selected, self.select_predictive = Gui_Tools.create_combobox(self.master,
                                                            "Select the Predictive Analytics: ",
                                                            self.predictive)

        # Create button to quit program, Handler for button click is self.quit
        Gui_Tools.create_button(master, "Quit", "#2B547E", "#EBF3FB", self.quit)

    def quit(self):
        self.master.destroy()

    def get_input(self):
        """ store user input for analytics """
        # error handling if either entry box is empty (cannot be empty)
        if len(self.stocktkr_entry.get()) == 0:
            msg.showinfo("Warning", \
            "Please enter a stock ticker")
        elif len(self.daysinfuture_entry.get()) == 0:
            msg.showinfo("Warning", \
            "Please enter a number between 0 and 20 for the prediction.")
        # error handling if future days entered
        # are outside of range between 0 and 20
        elif int(self.daysinfuture_entry.get()) < 0 or \
           int(self.daysinfuture_entry.get()) > 20:
            msg.showinfo("Wrong Input", \
            "Please enter a number between 0 and 20 for the prediction.")
        # error handling to ensure start date is before end date
        elif self.startdate.get_date() > self.enddate.get_date():
            msg.showinfo("Wrong Input", \
            "Please make sure the Start Date lies before the End Date.")
        else:
            # error handling if ticker not valid
            try:
                self.ticker_str = self.stocktkr_entry.get().upper()
                self.ticker = yf.Ticker(self.ticker_str)
                self.company_name = self.ticker.info["shortName"]
                # if all error tests pass, store data in variables for processing
                self.getdata_button_clicked = True
                self.populate_combobox()
                self.start_date = self.startdate.get_date()
                self.end_date = self.enddate.get_date()
                self.daysinfuture = int(self.daysinfuture_entry.get())
                # create dateframe with stock data based on user input
                self.stock_data = get_data(self.ticker, self.ticker_str,
                                    self.start_date, self.end_date)
                # instantiate graph to be used in analytics
                self.graph = Graphs(self.stock_data, self.ticker_str, self.company_name)
                # transform daysinfuture to business date in future
                # bank holidays not considered, only weekends
                self.date_daysinfuture = self.end_date + \
                                            timedelta(days=self.daysinfuture)
                while self.date_daysinfuture.weekday() > 4:
                    self.date_daysinfuture += timedelta(days=1)
                # show summary of data stored
                msg.showinfo("Data stored", "{} \n\nTicker {} \nStart Date: {} \
                             \nEnd  Date: {} \
                             \nDay(s) in the Future: {} -> bd {}".format(self.company_name,
                             self.ticker_str, self.start_date, self.end_date,
                             self.daysinfuture, self.date_daysinfuture))
                # return values for other functions
                return self.ticker_str, self.ticker, self.company_name
            except KeyError:
                msg.showinfo("Wrong Input", "Please enter a valid stock ticker.")

    def descriptive(self, event):
        """ process descriptive analytics """
        # https://www.delftstack.com/tutorial/tkinter-tutorial/tkinter-combobox/
        # check which option was selected and call respective function
        selected = self.str_descr_selected.get()
        # option 1
        if selected == "Data Overview":
            descriptive_stats(self.stock_data, self.ticker_str, self.ticker)
        # option 2
        elif selected == "Time Series - Price & Volume":
            self.graph.timeseries()
        # option 3
        elif selected == "Moving Average Cross":
            self.graph.ma_compare()
        # option 4
        elif selected == "Weighted MA vs Closing Price":
            self.graph.wma_vs_close()
        # option 5
        elif selected == "MACD":
            self.graph.macd()

    def predictive(self, event):
        """ process predictive analytics """

        num_data_points, lr, trendline, rmse = linear_reg(self.stock_data)
        # check which option was selected and call respective function
        selected = self.str_pred_selected.get()
        # option 1
        if selected == "Time Series with Linear Trend":
            self.graph.timeseries_trend(trendline)
        # option 2
        elif selected == "Predict the Future - LinReg":
            # calculate predicted closing price
            pred_val = predict_value(lr, num_data_points, self.daysinfuture)
            pred_list = predict_series(lr, num_data_points, self.daysinfuture)
            # print results + stastical confidence values in messagebox
            msg.showinfo("Prediction",
                         "Predicted Closing Price for {0}:\n{1}\
                         \nList of {2} predicted values from selected End Date:\
                         \n{3}".format(self.date_daysinfuture, pred_val,
                         self.daysinfuture, pred_list))
            if round(lr.rvalue**2,5) > 0.75 and rmse < 25:
                msg.showinfo("LinReg - Confidence",
                     "For a good model, the following should be true: \
                     \nR-Squared > 0.75 and RMSE < 25 \
                     \n\nR-Squared: {} \
                     \nRMSE: {} \
                     \nThe model seems decent.".format(round(lr.rvalue**2,5), rmse))
            else:
                msg.showinfo("LinReg - Confidence",
                     "For a good model, the following should be true: \
                     \nR-Squared > 0.75 and RMSE < 25 \
                     \n\nR-Squared: {} \
                     \nRMSE: {} \
                     \nMaybe you should not trust the prediction...\
                     \nperhaps if you choose a shorter, more recent time frame, the linear regression results would improve.".format(round(lr.rvalue**2,5), rmse))

    def populate_combobox(self):
        """ populate combobox in GUI """
        # Adding options to drop down in combobox for descriptive analytics
        self.select_descriptive["values"] = ("Data Overview",
                                             "Time Series - Price & Volume",
                                             "Moving Average Cross",
                                             "Weighted MA vs Closing Price",
                                             "MACD")
        # Adding options to drop down in combobox for predictive analytics
        self.select_predictive["values"] = ("Time Series with Linear Trend",
                                            "Predict the Future - LinReg")

class Gui_Tools:
    """ class to create various gui tools """
    # https://www.python-course.eu/tkinter_entry_widgets.ph
    def create_entrybox(master, label, row, col):
        tk.Label(master, text = label, font = ("Goldman Sans", 10),
                bg="#5991CA").grid(sticky="e", row = row, column = col)
        col +=1
        entrybox = tk.Entry(master, width=10)
        entrybox.grid(row = row, column = col)
        return entrybox

    def create_header(master, label, fontsize):
        tk.Label(master, text = label,
                 font = ("Goldman Sans", fontsize, "bold"),
                 bg="#5991CA").grid(columnspan=2)

    def create_dateentry(master, label, default_year, row, col):
        tk.Label(master, text = label, font = ("Goldman Sans", 10),
                bg="#5991CA").grid(row = row, column = col)
        col += 1
        dateentrybox = DateEntry(master, locale='en_US', date_pattern='dd-MM-yyyy',
                        width=10, bg="darkblue", fg="white", year = default_year)
        dateentrybox.grid(sticky="w", row = row,column = col)
        return dateentrybox

    def create_combobox(master, label, function):
        # combobox label
        tk.Label(master, text = label,
                font = ("Goldman Sans", 11, "bold"), bg="#5991CA").grid(columnspan=2)
        # create combobox
        combobox_selected = tk.StringVar()
        combobox = ttk.Combobox(master, width = 30, textvariable = combobox_selected)
        combobox.grid(columnspan=2)
        combobox.bind("<<ComboboxSelected>>", function)
        return combobox_selected, combobox

    def create_button(master, label, button_color, label_color, function):
        tk.Button(master, text = label, bg = button_color,
                  fg = label_color, command = function, width = 10).grid(columnspan=2)
