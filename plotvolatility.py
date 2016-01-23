#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Copyright 2016 Enrico Polesel all rights reserved
# TODO: license

import gethistory
import json
import datetime
import matplotlib.pyplot as plt

def plot_volatility(symbol,startyear,endyear):
    startyear = int(startyear)
    endyear = int(endyear)
    volatilities = {}
    prices = {}
    dates = []
    for year in range(startyear,endyear+1):
        print(year)
        data = gethistory.get_history(datetime.date(year,1,1),datetime.date(year,12,31),[symbol])
        for quote in data[symbol]:
            date = datetime.datetime.strptime(quote['Date'],"%Y-%m-%d")
            dates.append(date)
            volatilities[date] = (float(quote['High']) - float(quote['Low']))/2/float(quote['Open'])
            prices[date] = float(quote['Open'])
    print(len(dates))
    fig, ax1 = plt.subplots()
    ax1.plot(dates,[volatilities[date] for date in dates ],'r')
    ax1.set_xlabel('time')
    ax1.set_ylabel('volatility',color='r')
    ax2 = ax1.twinx()
    ax2.plot(dates,[prices[date] for date in dates ],'b')
    ax2.set_ylabel('price',color='b')
    
#    plt.plot(dates,[volatilities[date] for date in dates ],'r',dates,
    plt.show()
    

if __name__ == "__main__":
    plot_volatility("BMPS.MI",2014,2016)
        
