import subprocess

def getDataFromWhatWeb(url, cookie, token):
    
    reportName = 'whatweb_' + token + '.report'
    subprocess.run(['rm', reportName], cwd='/root/python_tool/whatweb_tool')

    if (cookie != None):
        results = subprocess.run(['whatweb','-a','3','--log-xml', reportName,'-t','20','--cookie',cookie,url], capture_output=True, cwd='/root/python_tool/whatweb_tool')
    else:
        results = subprocess.run(['whatweb','-a','3','--log-xml', reportName,'-t','20',url], capture_output=True, cwd='/root/python_tool/whatweb_tool')

    if (results.returncode != 1):
        return True
    else:
        return False
