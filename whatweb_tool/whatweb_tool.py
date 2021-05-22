import subprocess

def getDataFromWhatWeb(url, cookie, token):
    
    #subprocess.run(['rm','whatweb_results.xml'])
    reportName = 'whatweb_' + token + '.report'
    if (cookie != None):
        results = subprocess.run(['whatweb','-a','3','--log-xml', reportName,'-t','20','--cookie',cookie,url], capture_output=True, cwd='/root/python_tool/whatweb_tool')
    else:
        results = subprocess.run(['whatweb','-a','3','--log-xml', reportName,'-t','20',url], capture_output=True, cwd='/root/python_tool/whatweb_tool')

    if (results.returncode != 1):
        return True
    else:
        return False
