import os
import re
import json
from bs4 import BeautifulSoup

# Get report path
path = '/root/python_tool/joomscan/reports/'
reportFolder = os.listdir(path)[0]
reportPath = os.path.join(path,reportFolder)

def parseReportHTML(htmlCode):
    soup = BeautifulSoup(htmlCode, 'html.parser')
    results = {}

    # Brief information about report
    listTag = ['url','version','start', 'finish']
    briefInfs = soup.find_all('div')[1].find_all('span')

    for briefInf in briefInfs:
        results[listTag[briefInfs.index(briefInf)]] = briefInf.text
    
    # Detailed information in report
    detailInfs = soup.find_all('tr')
    for detailInf in detailInfs[1:]:
        key = detailInf.h3.text.replace('[+] ','')
        results[key] = []
        tmp = {}
        for child in detailInf.p.children:
            try:
                print(child.text)
            except:
                print(child)
            try:
                tmp['inf'] = child.text
            except:
                tmp['inf'] = child
        results[key].append(tmp)
    # print(json.dumps(results))


def getJsonData():
    for reportFile in os.listdir(reportPath):
        if re.search("(.html)$", reportFile):
            with open(os.path.join(reportPath,reportFile), 'r') as f:
                results = parseReportHTML(f.read())
                return results

print(getJsonData())