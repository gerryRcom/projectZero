#!./bin/python
# pip install yfinance
import requests
import sys
import sqlite3
from bs4 import BeautifulSoup
import json
import subprocess
import os.path
from datetime import date, timedelta
import yfinance as yf

# Check that the required SQLite DB exists and connect, if not, exit the script.
projectZeroDB='projectZeroDB.db'
if not os.path.exists(projectZeroDB):
    sys.exit("Database does not exist, exiting")
else:
    # connect to DB to pull info to query
    dbConnect = sqlite3.connect(projectZeroDB)
    dbCurser = dbConnect.cursor()

# Loop through last X days of data
x = 5
while x > 0: 
    today = date.today() - timedelta(days=x)
    todayDB = today.isoformat()

    dbContent = dbCurser.execute('SELECT * FROM projectZeroNews WHERE date =(?)',(todayDB,))
    for row in dbContent:
        print(str(row))
    x-=1

msft = yf.Ticker("MSFT")

# get all stock info
msft.info

# get historical market data
hist = msft.history(period="5d")
print(hist['High'])

# Close DB connection
dbConnect.close()
