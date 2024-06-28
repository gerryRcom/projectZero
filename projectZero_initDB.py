#!./bin/python
# Run script to initialise a new DB for projectZero or print contents if it exists.
import os.path
import sqlite3
import sys

projectZeroDB='projectZeroDB.db'

# check if database file exists, if it does print all content (for troubleshooting)
if os.path.exists(projectZeroDB):
    dbConnect = sqlite3.connect(projectZeroDB)
    dbCurser = dbConnect.cursor()
    dbContent = dbCurser.execute("SELECT * FROM projectZeroNews")
    print(dbContent.fetchall())
    dbContent = dbCurser.execute("SELECT * FROM projectZeroTickers")
    print(dbContent.fetchall())
    dbConnect.close()
    sys.exit()
# if the database file doesn't exist create required tables
else:
    dbConnect = sqlite3.connect(projectZeroDB)
    dbCurser = dbConnect.cursor()
    dbCurser.execute("CREATE TABLE projectZeroNews(date, headline, UNIQUE(headline))")
    dbConnect.commit()
    dbCurser.execute("CREATE TABLE projectZeroTickers(date, ticker, status)")
    dbConnect.commit()
    dbConnect.close()
    # confirm DB exists (in case create above failed/ did not complete)
    if os.path.exists(projectZeroDB):
        sys.exit()
    else:
        sys.exit("Database does not exist, exiting")