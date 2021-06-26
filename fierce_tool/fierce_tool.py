import subprocess
import sys
from tldextract import extract
from pids import pids_of_token

def getDataFromFierce(url, token):

    tsd, td, tsu = extract(url)
    url = td + '.' + tsu
    
    reportName = 'fierce_' + token + '.report'

    # Delete duplicate file
    subprocess.run(['rm', reportName], cwd='/root/python_tool/fierce/')
    if (token in pids_of_token.keys()):
        process = subprocess.Popen(['perl','fierce.pl','-file', reportName,'-dns',url], cwd='/root/python_tool/fierce', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            pids_of_token[token].append(process.pid)
            process.wait()

            if (token in pids_of_token.keys()):
                pids_of_token[token].remove(process.pid)
                re, err = process.communicate()
                if (process.returncode != 1):
                    return True
                else:
                    return False
            return False
        except:
            return False

    return False
