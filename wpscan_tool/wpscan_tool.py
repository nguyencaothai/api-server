import subprocess
from pids import pids_of_token

def getDataFromWpscan(url, cookie, token):
    
    reportName = 'wpscan_' + token + '.report'

    subprocess.run(['rm',reportName], cwd='/root/python_tool/wpscan_tool/')

    if (token in pids_of_token.keys()):
        if (cookie != None):
            process = subprocess.Popen(['wpscan','--no-banner','-e','ap,at,cb','--detection-mode','mixed','--plugins-detection','mixed','--url',url,'--cookie-string',cookie,'-t','10','-f','json','-o', reportName], cwd='/root/python_tool/wpscan_tool', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # proces = subprocess.Popen(['wpscan','--no-banner','-e','ap,at,cb','--url',url,'--cookie-string',cookie,'-t','100','-f','json','-o','wpscan.json'],capture_output=True)

        else:
            process = subprocess.Popen(['wpscan','--no-banner','-e','ap,at,cb','--detection-mode','mixed','--plugins-detection','mixed','--url',url,'-t','10','-f','json','-o', reportName], cwd='/root/python_tool/wpscan_tool', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # proces = subprocess.Popen(['wpscan','--no-banner','-e','ap,at,cb','--url',url,'-t','100','-f','json','-o','wpscan.json'],capture_output=True)
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
