import subprocess
import sys
from tldextract import extract

def getDataFromFierce(url, token):

    tsd, td, tsu = extract(url)
    url = td + '.' + tsu
    
    reportName = 'fierce_' + token + '.report'

    # Delete duplicate file
    subprocess.run(['rm', reportName], cwd='/root/python_tool/fierce/')

    results = subprocess.run(['perl','fierce.pl','-file', reportName,'-dns',url], cwd='/root/python_tool/fierce', capture_output=True)
    if (results.returncode != 1):
        return True
    else:
        return False
