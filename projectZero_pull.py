#!./bin/python
# pip install beautifulsoup4 requests lxml
import requests
import sys
import re
from bs4 import BeautifulSoup
import sqlite3
import os.path
from datetime import date

# Check that the required SQLite DB exists and connect, if not, exit the script.
projectZeroDB='projectZeroDB.db'
if not os.path.exists(projectZeroDB):
    sys.exit("Database does not exist, exiting")
else:
    dbConnect = sqlite3.connect(projectZeroDB)
    dbCurser = dbConnect.cursor()

# Get date for DB entries
today = date.today()
todayDB = today.isoformat()

# List of urls and site specific code/tag to use as the ID to extract the appropriate content
dataSource= {
    "https://www.ft.com/rss/home/uk": "description",
    "https://www.cnbc.com/id/19746125/device/rss/rss.xml": "description",
    "https://seekingalpha.com/market_currents.xml": "title",
    "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147": "description",
    "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839135": "description"
    #"https://www.bbc.com/news/business/companies": "ssrcss-9haqql-LinkPostLink ej9ium92",
    #"https://www.reuters.com/business/": "",
    #"https://finance.yahoo.com/topic/stock-market-news": "Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled"
}

# iterate through sites and search for required content to parse to DB.
for key, value in dataSource.items():
    sourceSite=key
    sourceID=value
    sourceContent = requests.get(sourceSite)
    # Scrape the site using bs4 and extract required content based on pre-determined tag
    soup = BeautifulSoup(sourceContent.content, "xml")
    sourceContent = soup.find_all(sourceID)
    for content in sourceContent:
        tempContent = str(content)
        tempContent = tempContent.rsplit("<", 1)[-2]
        keyContent = tempContent.rsplit(">", 1)[-1]
        # pass the extracted headlines to sqlite3 db
        dbCurser.execute("INSERT OR IGNORE INTO projectZeroNews(date, headline) VALUES(?, ?)",(todayDB, keyContent))
        dbConnect.commit()
        print(keyContent)

# Close DB connection
dbConnect.close()
