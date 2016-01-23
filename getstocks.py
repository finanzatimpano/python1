#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Copyright 2016 Enrico Polesel all rights reserved
# TODO: license

import datetime
import urllib.parse
import urllib.request
import json
import csv

# symbols = ["YHOO", "AAPL", "GOOG", "MSFT"];

def yahoo_query(query):
	url = 'https://query.yahooapis.com/v1/public/yql?q='+urllib.parse.quote(query)+'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
    response = urllib.request.urlopen(url)
    response_str = response.readall().decode('utf-8')
    raw_data = json.loads(response_str)
    quotes = raw_data['query']['results']['quote']
    data = { symbol : [] for symbol in symbols }
    for quote in quotes:
        data[quote['Symbol']].append(quote);
    return data;

def get_stockprice(symbols):
	query = 'select * from yahoo.finance.quotes where symbol in ({symbols})'.format(symbols=','.join([ '"'+symbol+'"' for symbol in symbols]))
    data = yahoo_query(query);
    for key in data.keys():
		with open(key+'-continuous.csv', 'w') as csvout:
			writer = csv.writer(csvout);
			columns = ['Ask', 'Bid', 'LastTradeWithTime', 'ShortRatio', 'Volume'];
			# Scrivere ste cose sul file (EPOL lo FA)
			csvout.close();
    
def get_dailyvalues(symbols):
	query = 'select * from yahoo.finance.quotes where symbol in ({symbols})'.format(symbols=','.join([ '"'+symbol+'"' for symbol in symbols]))
	data = yahoo_query(query);
	for key in data.keys():
		with open(key+'-daily.csv', 'w') as csvout:
			writer = csv.writer(csvout);
			columns = ['AverageDailyVolume', 'BookValue', 'DaysLow', 'DaysHigh', 'LastTradeWithTime', 'Open', 'PreviousClose'];
			# Scrivere ste cose sul file (EPOL lo FA)
			csvout.close();

if __name__ == "__main__":
    for year in range(2000,2017):
        get_year(year)
