import subprocess
from pids import pids_of_token

def getDataFromWafw00f(url, token):

    reportName = 'wafw00f_' + token + '.report'
    subprocess.run(['rm', reportName], cwd='/root/python_tool/wafw00f_tool')

    if (token in pids_of_token.keys()):
        process = subprocess.Popen(['wafw00f','-a', '-f','json', '-o', reportName,url], cwd='/root/python_tool/wafw00f_tool/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
            return False
        except:
            return False

    return False
