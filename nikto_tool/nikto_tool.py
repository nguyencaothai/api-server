import subprocess
import json
import os

def getDataFromNikto(url, token):

    # subprocess.run(['rm','nikto_results.json'])

    reportName = 'nikto_' + token + '.report'    
    results = subprocess.run(['nikto','-h',url,'-Format','json', '-o', reportName, '-maxtime', '600s'], capture_output=True, cwd='/root/python_tool/nikto_tool/')
    if (results.returncode != 1):
        return True
    else:
        return False