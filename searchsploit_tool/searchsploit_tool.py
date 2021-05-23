import subprocess
import json

def getDataFromSearchsploit(pattern):
    
    results = subprocess.run(['searchsploit','-t',pattern,'--json'] ,capture_output=True)
    if (results.returncode != 1):
        return results.stdout
    else:
        return "Error"

