import pandas as pd
import requests
import datetime
import logging
import curlify
import traceback


url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
instrumentList3 = pd.read_csv(url, compression="gzip")

def get_dataToken_upstox(tradesymbol,exchange="NFO"):
  if exchange == "NFO":
    exchange = "NSE_FO"
  if exchange == "NSE":
    exchange = "NSE_EQ"
  if exchange == "MCX":
    exchange = "MCX_FO"
  if exchange == "BFO":
    exchange = "BSE_FO"
  if exchange == "BSE":
    exchange = "BSE_EQ"
  dataToken = instrumentList3[(instrumentList3["tradingsymbol"]==tradesymbol) & (instrumentList3["exchange"]==exchange)]
  return dataToken.instrument_key.iloc[0]