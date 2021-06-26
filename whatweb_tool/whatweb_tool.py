import subprocess
from pids import pids_of_token

def getDataFromWhatWeb(url, cookie, token):
    
    reportName = 'whatweb_' + token + '.report'
    subprocess.run(['rm', reportName], cwd='/root/python_tool/whatweb_tool/')

    if (token in pids_of_token.keys()):
        if (cookie != None):
            process = subprocess.Popen(['whatweb','-a','3','--log-xml', reportName,'-t','10','--cookie',cookie,url], cwd='/root/python_tool/whatweb_tool', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            process = subprocess.Popen(['whatweb','-a','3','--log-xml', reportName,'-t','10',url], cwd='/root/python_tool/whatweb_tool', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            pids_of_token[token].append(process.pid)
            process.wait()
            
            if (token in pids_of_token.keys()):
                pids_of_token[token].remove(process.pid)
                re, err = process.communicate()
                if (process.returncode != 1):
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False
            
    return False
