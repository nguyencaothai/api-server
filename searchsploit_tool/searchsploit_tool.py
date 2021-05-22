import subprocess
import json

def getDataFromSearchsploit(pattern):

    subprocess.run(['rm','searchsploit_results.json'])
    
    results = subprocess.run(['searchsploit',pattern,'--json'] , capture_output = True)
    if (results.returncode != 1):
        return results.stdout
    else:
        return "Error"