import subprocess
import json
import os

def getDataFromNikto(url):

    subprocess.run(['rm','nikto_results.json'])
        
    results = subprocess.run(['nikto','-h',url,'-Format','json', '-o', 'nikto_results.json', '-maxtime', '600s'], capture_output=True)
    if (results.returncode != 1):
        return True
    else:
        return False