#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Copyright 2016 Enrico Polesel all rights reserved
# TODO: license

import datetime
import urllib.parse
import urllib.request
import json
import csv
import argparse


def yahoo_query(query):
    url = 'https://query.yahooapis.com/v1/public/yql?q='+urllib.parse.quote(query)+'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
    response = urllib.request.urlopen(url)
    response_str = response.readall().decode('utf-8')
    raw_data = json.loads(response_str)
    quotes = raw_data['query']['results']['quote']
#    data = { symbol : [] for symbol in symbols }
    data = {}
    for quote in quotes:
        if quote['Symbol'] not in data:
            data[quote['Symbol']] = []
        data[quote['Symbol']].append(quote)
    return data;

def get_stockprice(symbols):
    query = 'select * from yahoo.finance.quotes where symbol in ({symbols})'.format(symbols=','.join([ '"'+symbol+'"' for symbol in symbols]))
    columns = ['Ask', 'Bid', 'LastTradeWithTime', 'ShortRatio', 'Volume'];
    data = yahoo_query(query);
    for key in data.keys():
        filename = key+'-continuous.csv'
        try:
            csvout = open(filename,'r')
        except:
            csvout = open(filename,'w')
            writer = csv.writer(csvout)
            writer.writerow(columns)
        csvout.close()
        with open(filename, 'a') as csvout:
            writer = csv.writer(csvout)
            for quote in data[key]:
                writer.writerow([quote[field] for field in columns])
            csvout.close();


def get_dailyvalues(symbols):
    query = 'select * from yahoo.finance.quotes where symbol in ({symbols})'.format(symbols=','.join([ '"'+symbol+'"' for symbol in symbols]))
    data = yahoo_query(query);
    columns = ['AverageDailyVolume', 'BookValue', 'DaysLow', 'DaysHigh', 'LastTradeWithTime', 'Open', 'PreviousClose'];
    for key in data.keys():
        filename = key+'-daily.csv'
        try:
            csvout = open(filename,'r')
        except:
            csvout = open(filename,'w')
            writer = csv.writer(csvout)
            writer.writerow(columns)
        csvout.close()
        with open(filename, 'a') as csvout:
            writer = csv.writer(csvout)
            for quote in data[key]:
                writer.writerow([quote[field] for field in columns])
            csvout.close()


def main():
#    symbols = ["YHOO", "AAPL", "GOOG", "MSFT"]
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--daily",help="Get daily data",action="store_true")
    parser.add_argument("symbols",help="Symbols to monitor",nargs='+')
    args = parser.parse_args()
    if args.daily:
        get_dailyvalues(args.symbols)
    else:
        get_stockprice(args.symbols)


if __name__ == "__main__":
    main()
