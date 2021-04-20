import subprocess

def getDataFromWhatWeb(url, cookie):
    
    subprocess.run(['rm','whatweb_results.xml'])
    if (cookie != None):
        results = subprocess.run(['whatweb','-a','3','--log-xml','whatweb_results.xml','-t','100','--cookie',cookie,url], capture_output=True)
    else:
        results = subprocess.run(['whatweb','-a','3','--log-xml','whatweb_results.xml','-t','100',url], capture_output=True)

    if (results.returncode != 1):
        return True
    else:
        return False

