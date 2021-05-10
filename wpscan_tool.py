import subprocess

def getDataFromWpscan(url, cookie):
    
    if (cookie != None):
        results = subprocess.run(['wpscan','--no-banner','-e','ap,at,cb','--detection-mode','mixed','--plugins-detection','mixed','--url',url,'--cookie-string',cookie,'-t','100','-f','json','-o','wpscan.json'],capture_output=True)
        # results = subprocess.run(['wpscan','--no-banner','-e','ap,at,cb','--url',url,'--cookie-string',cookie,'-t','100','-f','json','-o','wpscan.json'],capture_output=True)

    else:
        results = subprocess.run(['wpscan','--no-banner','-e','ap,at,cb','--detection-mode','mixed','--plugins-detection','mixed','--url',url,'-t','100','-f','json','-o','wpscan.json'],capture_output=True)
        # results = subprocess.run(['wpscan','--no-banner','-e','ap,at,cb','--url',url,'-t','100','-f','json','-o','wpscan.json'],capture_output=True)
        
    if (results.returncode != 1):
        return True
    else:
        return False
