import subprocess

def getDataFromWpscan(url, cookie):
    
    if (cookie != None):
        results = subprocess.run(['wpscan','--url',url,'--cookie-string',cookie,'-t','50','--detection-mode','aggressive','-f','json','-o','wpscan.json'],capture_output=True)
    else:
        results = subprocess.run(['wpscan','--url',url,'-t','50','--detection-mode','aggressive','-f','json','-o','wpscan.json'],capture_output=True)
        
    if (results.returncode != 1):
        return True
    else:
        return False
