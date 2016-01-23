#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Copyright 2016 Enrico Polesel all rights reserved
# TODO: license

import datetime
import urllib.parse
import urllib.request
import json
import csv


def get_history(firstday,lastday,symbols):
    query = 'select * from yahoo.finance.historicaldata where symbol in ({symbols}) and startDate = "{startdate}" and endDate = "{enddate}"'.format(startdate=firstday.strftime("%Y-%m-%d"),enddate=lastday.strftime("%Y-%m-%d"),symbols=','.join([ '"'+symbol+'"' for symbol in symbols]))
    url = 'https://query.yahooapis.com/v1/public/yql?q='+urllib.parse.quote(query)+'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
    response = urllib.request.urlopen(url)
    response_str = response.readall().decode('utf-8')
    raw_data = json.loads(response_str)
    quotes = raw_data['query']['results']['quote']
    data = { symbol : [] for symbol in symbols }
    for quote in quotes:
        data[quote['Symbol']].append(quote)
    for key in data.keys():
        data[key].sort(key=lambda quote: quote['Date'])
    return data



def save_year(year):
    year = int(year)
    data = get_history(datetime.date(year,1,1),datetime.date(year,12,31),['YHOO','RACE.MI','LUX.MI'])
    for key in data.keys():
        with open(key+str(year)+'.csv','w') as csvout:
            writer = csv.writer(csvout)
            columns = ['Date','Open','Close','High','Low','Volume']
            writer.writerow(columns)
            for quote in data[key]:
                writer.writerow([quote[field] for field in columns])
            csvout.close()


if __name__ == "__main__":
    for year in range(2000,2017):
        get_year(year)
