import subprocess
import json

def getDataFromSearchsploit(pattern):

    subprocess.run(['rm','searchsploit_results.json'])
    
    with open('searchsploit_results.json','w') as f:
        results = subprocess.run(['searchsploit',pattern,'--json'], stdout=f)
    if (results.returncode != 1):
        return True
    else:
        return False