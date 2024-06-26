#!./bin/python
# pip install beautifulsoup4 requests lxml
import requests
import sys
import sqlite3
from bs4 import BeautifulSoup
import json
import subprocess
import os.path
from datetime import date

# Check that the required SQLite DB exists and connect, if not, exit the script.
projectZeroDB='projectZeroDB.db'
if not os.path.exists(projectZeroDB):
    sys.exit("Database does not exist, exiting")
else:
    # connect to DB to pull info to query
    dbConnect = sqlite3.connect(projectZeroDB)
    dbCurser = dbConnect.cursor()
    
    # Launch local llm to process info (manually doing this atm)
    # llmProcess = subprocess.Popen("./ollama serve", shell=True)
    # llmModel = subprocess.Popen("./ollama run mistral", shell=True)

# Get date for DB entries
today = date.today()
todayDB = today.isoformat()

# Get todays content from DB to pass to llm for processing
dbContent = dbCurser.execute('SELECT * FROM projectZeroNews WHERE date =(?)',(todayDB,))
for row in dbContent:
    print(row[1]) # Where 2 is the X column
    # t up the prompts to pass to the llm
    sourceQuestion1 = {
        "model": "mistral",
        "prompt": "answer in one word whether this statemet is positive or negative news for the company: "+str(row),
        "stream": False
    }
    sourceQuestion2 = {
        "model": "mistral",
        "prompt": "reply with a single word only, the first word should be the company's stock exchange symbol of the company mentioned in this statement, for example: Tesla would be TSLA: "+str(row),
        "stream": False
    }
    sourceHeader = {
        "Content-Type": "application/json"
    }
    # pass two queries to local llm 
    sourceContent1 = requests.post("http://localhost:11434/api/generate", headers=sourceHeader, data=json.dumps(sourceQuestion1))
    sourceContent2 = requests.post("http://localhost:11434/api/generate", headers=sourceHeader, data=json.dumps(sourceQuestion2))
    
    # extract the specific part of the response required
    llmResponseData1 = sourceContent1.text
    llmResponseData2 = sourceContent2.text
    llmResponseJSON1 = json.loads(llmResponseData1)
    llmResponseJSON2 = json.loads(llmResponseData2)
    llmResponseText1 = llmResponseJSON1["response"]
    llmResponseText2 = llmResponseJSON2["response"]
    llmStatus = llmResponseText1.split(' ')[1]
    llmTicker = llmResponseText2.split(' ')[1]
    print(llmStatus)
    print(llmTicker)

    # only save replies to the DB that have a reasonable chance of being accurate
    if llmStatus == "Negative" or llmStatus == "Positive":
        if len(llmTicker) >= 1 and len(llmTicker) <= 5:
            dbConnect.execute("INSERT INTO projectZeroTickers(date, ticker, status) VALUES(?, ?, ?)",(todayDB, llmStatus, llmTicker))
            dbConnect.commit()

# Close DB connection
dbConnect.close()
