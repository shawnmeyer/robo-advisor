#robo_advisor.py

#import modules
import datetime
import os
import requests
import json
import csv

from os.path import join, dirname
from dotenv import load_dotenv

#take key from hidden .env file
env_path = join(dirname(__file__),'..', '.env')
load_dotenv(env_path)

secret_key = os.getenv("ALPHADVANTAGE_API_KEY")

#GET method for getting stock spot info from Alphadvantage
def get_ticker_info(stock):
    ticker_info = requests.get(api_url_base + stock + url_ask_api + api_key)

    if ticker_info.status_code == 200:
        results = ticker_info.json()
        return results
    else:
        print(ticker_info.status_code)
        return None

#GET method for getting stock historical data from Alphadvantage
def get_price_history(stock):
    price_history = requests.get(api_historic_base + stock + url_ask_api + api_key)

    if price_history.status_code == 200:
        results = json.loads(price_history.text)
        return results
    else:
        print("The following error has occurred: ") #Validate API request to Alphadvantage
        print(price_history.status_code)
        exit()
        return None

#method for calculating highest price in recent 100 days.
def hi(price_list):
    local_hi = 0

    for x in price_list.values():
        if float(x["2. high"]) > local_hi:
            local_hi = float(x["2. high"])
    
    return local_hi

#method for calculating lowest price in recent 100 days.
def lo(price_list):
    local_lo = 999999999

    for x in price_list.values():
        if float(x["3. low"]) < local_lo:
            local_lo = float(x["3. low"])
    
    return local_lo

api_key = secret_key
api_url_base = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol="
url_ask_api = "&apikey="
api_historic_base = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
lb = "------------------------------------------"

while True:
    stock_symbol = input("Please enter a valid ticker: ")
    if(stock_symbol.isalpha()): #validate that stock entered only utilizes alphabetic characters
        break
    print("Oops! This ticker is invalid.") 

stock_info = get_ticker_info(stock_symbol)
price_info = get_price_history(stock_symbol)
if "Error Message" in price_info: #validate that stock ticker entered exists and is tracked.
    print("Woops, that ticker isn't tracked by Alphavantage!")
    exit()

daily_info = price_info["Time Series (Daily)"]
csv_info = daily_info.values()
csv_columns = ["timestamp", "open", "high", "low", "close", "volume"]

#create .csv file with stock historical data.
with open(join(dirname(__file__),'..',"data","prices.csv"), "w") as prices:
    writer = csv.DictWriter(prices, fieldnames = csv_columns)
    writer.writeheader()

    for date, g in zip(daily_info, csv_info):
        writer.writerow({
            "timestamp": date,
            "open": g["1. open"],
            "high": g["2. high"],
            "low": g["3. low"],
            "close": g["4. close"],
            "volume": g["5. volume"]})

historic_hi = hi(daily_info)
historic_lo = lo(daily_info)

#print results of API information call regarding stock ticker
print(lb)
print(stock_symbol.upper())
currentDT = datetime.datetime.now()
print("This report was run on " + currentDT.strftime("%b %d, %Y") +
" at " + currentDT.strftime("%I:%M:%S %p"))
print(lb)
print("This information was last updated on " + stock_info["Global Quote"]["07. latest trading day"])
print("The latest closing price was: " + '${:,.2f}'.format(float(stock_info["Global Quote"]["08. previous close"])))
print("The high price over the last 100 days was " + '${:,.2f}'.format(historic_hi))
print("The low price over the last 100 days was " + '${:,.2f}'.format(historic_lo))

#if price is higher than 1.2x the most recent lowest amount, recommend to wait to buy.
if historic_lo * 1.2 < float(stock_info["Global Quote"]["08. previous close"]):
    print("Don't buy -- wait for a dip!")
else:
    print("Buy and hold!")
    
