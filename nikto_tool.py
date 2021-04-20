import subprocess
import json

def getDataFromNikto(url):

    subprocess.run(['rm','nikto_results.json'])
    
    results = subprocess.run(['nikto','-h',url,'-Format','json', '-o', 'nikto_results.json'], capture_output=True)
    if (results.returncode != 1):
        return True
    else:
        return False