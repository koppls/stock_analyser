# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 17:35:42 2020

Main program file for execution

@author: Sabine Kopplin
"""

import tkinter as tk
from tkcalendar import Calendar,DateEntry
import tkinter.messagebox as msg
import datetime
from plots import Graphs
from gui import StockAnalyser_Main
from data import get_data, descriptive_stats
from prediction import linear_reg, predict_value, predict_series

def main():
    # interact with program on cmd line
    print("\n\n\nWhen you are ready, the Stock Analyser GUI will launch.")
    user_choice = input("Are you ready? Then enter YES.    ")
    # only proceed once user enters YES
    while user_choice != "YES":
        user_choice = input("How about now?    ")

    print("Well, good for you.")
    # launch GUI
    root = tk.Tk()
    # Force a specific geometry
    root.geometry("275x320")
    StockAnalyser_Main(root)
    root.mainloop()

if __name__== "__main__":
    main()
