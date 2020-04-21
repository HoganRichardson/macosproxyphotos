import sys
import os
import sqlite3

def printPaths(db):
    db = sqlite3.connect(db)

    missing = db.execute("SELECT uuid, imagePath  FROM RKMaster where isMissing is 1")

    for image in missing:
        # Print the original linked file path
        print(image[1])

if __name__ == "__main__":
    database = sys.argv[1]
    printPaths(database)
