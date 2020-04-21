import sys
import os
import sqlite3
from shutil import copy2

def extractPhotos (db, proxy_dir, out_dir):
    proxy_dir = proxy_dir + "/derivatives"
    db = sqlite3.connect(db)

    missing = db.execute("SELECT uuid, originalFileName FROM RKMaster where isMissing is 1")

    for image in missing:
        # Retrieve hex code in filename
        masterUuid = image[0]
        originalFileName = image[1]

        proxyId = db.execute("SELECT * FROM RKVersion where masterUuid is (?) LIMIT 1", [masterUuid]).fetchone()
        filename = str(format(proxyId[0], 'x'))

        # Search `proxy_dir` for filename, and copy to `./exports/*.*`
        for root, dirs, files in os.walk(proxy_dir):
            for name in files:
                if filename in name:
                    # Copy to tmp directory
                    print(name)
                    sourcePath = os.path.join(root, name)
                    destPath = os.path.join(out_dir, originalFileName) + "_" + name
                    copy2(sourcePath, destPath)

if __name__ == "__main__":
    database = sys.argv[1]
    proxy_dir = sys.argv[2]
    out_dir = sys.argv[3]

    extractPhotos(database, proxy_dir, out_dir)
