#!./bin/python
# Run script to initialise a new DB for projectZero or dump contents if it exists.
import os.path
import sqlite3
import sys

projectZeroDB='projectZeroDB.db'

if os.path.exists(projectZeroDB):
    dbConnect = sqlite3.connect(projectZeroDB)
    dbCurser = dbConnect.cursor()
    dbContent = dbCurser.execute("SELECT * FROM projectZeroNews")
    print(dbContent.fetchall())
    dbConnect.close()
    sys.exit()
else:
    dbConnect = sqlite3.connect(projectZeroDB)
    dbCurser = dbConnect.cursor()
    dbCurser.execute("CREATE TABLE projectZeroNews(date, headline, UNIQUE(headline))")
    dbConnect.commit()
    dbConnect.close()
    if os.path.exists(projectZeroDB):
        sys.exit()
    else:
        sys.exit("Database does not exist, exiting")