import subprocess

def getDataFromWpscan(url, cookie, token):
    
    reportName = 'wpscan_' + token + '.report'

    subprocess.run(['rm',reportName], cwd='/root/python_tool/wpscan_tool/')

    if (cookie != None):
        results = subprocess.run(['wpscan','--no-banner','-e','ap,at,cb','--detection-mode','mixed','--plugins-detection','mixed','--url',url,'--cookie-string',cookie,'-t','10','-f','json','-o', reportName],capture_output=True, cwd='/root/python_tool/wpscan_tool')
        # results = subprocess.run(['wpscan','--no-banner','-e','ap,at,cb','--url',url,'--cookie-string',cookie,'-t','100','-f','json','-o','wpscan.json'],capture_output=True)

    else:
        results = subprocess.run(['wpscan','--no-banner','-e','ap,at,cb','--detection-mode','mixed','--plugins-detection','mixed','--url',url,'-t','10','-f','json','-o', reportName],capture_output=True, cwd='/root/python_tool/wpscan_tool')
        # results = subprocess.run(['wpscan','--no-banner','-e','ap,at,cb','--url',url,'-t','100','-f','json','-o','wpscan.json'],capture_output=True)
        
    if (results.returncode != 1):
        return True
    else:
        return False
