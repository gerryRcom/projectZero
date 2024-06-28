#!./bin/python
# pip install yfinance
import sys
import sqlite3
import os.path
from datetime import date, timedelta
import yfinance as yf

# Check that the required SQLite DB exists and connect, if not, exit the script.
projectZeroDB='projectZeroDB.db'
if not os.path.exists(projectZeroDB):
    sys.exit("Database does not exist, exiting")
else:
    # Connect to DB to pull info to query
    dbConnect = sqlite3.connect(projectZeroDB)
    dbCurser = dbConnect.cursor()

# Loop through last X days of data and pass count of positive stock's stories to dictionary
tickerCount = {}
x = 5
while x >= 0: 
    today = date.today() - timedelta(days=x)
    todayDB = today.isoformat()

    # select tickers from DB for specific date, only extract Positive stocks.
    dbContent = dbCurser.execute('SELECT * FROM projectZeroTickers WHERE date =(?)',(todayDB,))
    for row in dbContent:
        if row[1] == "Positive":
            # save the ticker and count of occurances
            tickerCount.setdefault(row[2], 0)
            tickerCount[row[2]] += 1
            print(str(row))
        else:
            continue
    x=x-1

# loop through the ticker count dictionary and query stock if there was more than one occurance
for key, value in tickerCount.items():
    if value > 1:
        ytick = yf.Ticker(key)
        try:
            hist = ytick.history(period="1mo")
            # jump to next stock if no history found (e.g. invalid ticker)
            if hist.empty:
                continue
            else:
                # print 1 month stock histroy if returned
                print("{} is {}:".format(key, value))
                print((hist['High']))
        except:
            continue


# print ticker count dictionary content for review    
# print(tickerCount)

# Close DB connection
dbConnect.close()
