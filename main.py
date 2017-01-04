# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 09:58:06 2017

@author: Jason
"""

import pandas as pd
from pandas_datareader import data as web
from pandas_datareader._utils import RemoteDataError
import datetime


def update_data(sym,source):
    file_sym = sym.replace('^','')
    try:
        df1 = pd.read_csv('%s.csv'%file_sym)
        start = datetime.datetime.strptime(df1.iloc[-1].Date,'%Y-%m-%d') + \
                datetime.timedelta(days=1)
        print('Previous data found. Appending all new data')
    except FileNotFoundError:
        print('File does not exist, gathering all data and creating new file')  
        df1 = pd.DataFrame()
        start = datetime.datetime(1900,1,30)
    end = None
    if start.date() != datetime.datetime.now().date():
        try:
            df = web.DataReader(sym,source,start,end).round(2)
        except RemoteDataError:
            df = _get_cboe_data(sym)
            df = df[df.index > df1.iloc[-1,0]]
        if not df.empty:
            if df1.empty:
                df.to_csv('%s.csv'%file_sym)
            else:
                df.to_csv('%s.csv'%file_sym,mode='a',header=None)
        print('%s updated' % file_sym)
    else:
        print('%s already up to date. Skipping' % file_sym)

def _get_cboe_data(sym):
    df = pd.read_csv(_get_cboe_url(sym),skiprows=3)
    df['Date'] = pd.to_datetime(df.Date.str.replace('*',''))
    return df.set_index('Date') 
        
def _get_cboe_url(sym):
    urls = {'^VXST':'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vxstcurrent.csv'
            }
    return urls[sym]
            
if __name__=='__main__':
    syms = ['VXX','^VIX','^VXV','^VXST','SPY']
    src = 'yahoo'
    for sym in syms:
        update_data(sym,src)
        

        
