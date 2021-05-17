import os
import re
import json
from bs4 import BeautifulSoup

def parseReportHTML(htmlCode):
    soup = BeautifulSoup(htmlCode, 'html.parser')
    results = {}
    results['components'] = []
    results['version'] = ''
    
    # Get components for reports
    allH3tags = soup.find_all("h3",string=re.compile("Enumeration"))
    # print(allH3tags)
    for h3Tag in allH3tags:
        try:
            tmp = h3Tag.string.strip().split(' ')[3].replace('(','').replace(')','')
        except:
            tmp = ''
        # print(h3Tag.string.strip().split(' ')[3])
        if (tmp != ''):
            results['components'].append(tmp)
    
    # Get version of joomla
    version = soup.find(id="vbreport1")
    if (version.string != None):
        results['version'] = version.string.split()[1]

    return results

path = '/root/python_tool/joomscan/reports/'
reportFolder = os.listdir(path)[0]
reportPath = os.path.join(path, reportFolder)

for reportFile in os.listdir(reportPath):
    if re.search("(.html)$", reportFile):
        with open(os.path.join(reportPath, reportFile), 'r') as f:
            print(parseReportHTML(f.read()))