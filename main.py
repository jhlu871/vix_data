# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 09:58:06 2017

@author: Jason
"""

import pandas as pd
from pandas_datareader import data as web
import datetime


def update_data(sym,source):
    file_sym = sym.replace('^','')
    start = datetime.datetime(1900,1,30)
    end = None
    if not _get_cboe_url(sym):
        df = web.DataReader(sym,source,start,end).round(2)
    else:
        df = _get_cboe_data(sym)
    if not df.empty:
        df.to_csv('%s.csv'%file_sym)
    else:
        print('Error: no data for %s' % file_sym)
    print('%s updated' % file_sym)

def _get_cboe_data(sym):
    df = pd.read_csv(_get_cboe_url(sym),skiprows=3)
    df['Date'] = pd.to_datetime(df.Date.str.replace('*',''))
    return df.set_index('Date') 
        
def _get_cboe_url(sym):
    urls = {'^VXST':'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vxstcurrent.csv'
            }
    if sym in urls:
        return urls[sym]
    else:
        return None
            
if __name__=='__main__':
    syms = ['VXX','^VIX','^VXV','^VXST','SPY','^SP500TR']
    src = 'yahoo'
    for sym in syms:
        update_data(sym,src)
        

        
