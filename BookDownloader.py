# -*- coding: utf-8 -*-

import requests
import os
import re

# Downloads folder
BASEPATH = ""

def downloadBook(url, path):
    headers = {'Accept-Encoding': 'gzip, deflate, sdch','Accept-Language': 'en-US,en;q=0.8','Upgrade-Insecure-Requests': '1','User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Cache-Control': 'max-age=0','Connection': 'keep-alive'}
    r = requests.get(url, stream=True, headers=headers)
    if(not path.endswith('.pdf')):
        path=path+'.pdf'
    with open(path, "wb") as f:
        print("\nDownloading " + path)
        i=0
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                print('\r'+str(i)+'kb', end='')
                i=i+1
                f.write(chunk)
                
def createFolderIfNotExists(path):
    if(not os.path.exists(path)):
        os.mkdir(path)

# log for break-point
def readLog():
    try:
        with open('log') as f:
            s=int(f.read())
        return s
    except Exception as e:
        return 0

def writeLog(s):
    with open('log', 'w') as f:
        f.write(str(sig))

def deleteLogFile():
    try:
        os.remove('log')
    except Exception as e:
        pass

if __name__ == "__main__":
    urlPattern=re.compile("\[.*\]\((.*?)\)")
    with open("README.md") as f:
        path=BASEPATH
        # resume from break-point 
        sig=0
        log=readLog()
        for i in f:
            sig=sig+1
            # Create folder if it doesn't exist
            if(i.startswith("##") and not i.startswith("###")):
                path=os.path.join(BASEPATH, i[2:].strip())
                fatherPath=path
                createFolderIfNotExists(path)
            if(i.startswith("###")):
                path=os.path.join(fatherPath, i[3:].strip())
                createFolderIfNotExists(path)
            if(i.startswith('[')):
                url=re.findall(urlPattern, i)[0]
                fileName=url.split('/')[-1]
                try:
                    if(sig>=log):
                        downloadBook(url, os.path.join(path, fileName))
                except Exception as e:
                    # log break point
                    writeLog(sig)
                    raise e
    # delete log file when success
    deleteLogFile()
                

