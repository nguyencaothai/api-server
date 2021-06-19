import subprocess
import json
import os
from tldextract import extract

def getDataFromNikto(url, token):

    # subprocess.run(['rm','nikto_results.json'])

    reportName = 'nikto_' + token + '.report'    
    subprocess.run(['rm', reportName], cwd='/root/python_tool/nikto_tool')

    tsd, td, tsu = extract(url)
    url = tsd + '.' + td + '.' + tsu
    
    url = url[1: len(url)-1] if (url[0] == '.' and url[len(url)-1] == '.') else url[1:] if (url[0] == '.') else url[:len(url)-1] if (url[len(url)-1] == '.') else url
    
    port = '80'
    if "http://" in url:
        port = '80'
    if "https://" in url:
        port = '443'
    
    results = subprocess.run(['nikto','-h', url, '-p', port, '-Format','json', '-o', reportName, '-maxtime', '600s'], capture_output=True, cwd='/root/python_tool/nikto_tool/')
    if (results.returncode != 1):
        return True
    else:
        return False