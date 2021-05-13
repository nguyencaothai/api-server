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
    for h3Tag in allH3tags:
        tmp = h3Tag.string.strip().split(' ')[3].replace('(','').replace(')','')
        if (tmp != ''):
            results['components'].append(tmp)
    
    # Get version of joomla
    version = soup.find(id="vbreport1")
    if (version.string != None):
        results['version'] = version.string.split()[1]

    return results