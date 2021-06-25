import subprocess, re, os
from tldextract import extract
from pids import pids_of_token

def init_result_dir(url):
    ### initiate log directory and stuffs
    ## trim the url to use as a suitable directory Name
    if "http://" in url:
        url = url.replace('http://', '')
    elif "https://" in url:
        url = url.replace('https://', '')
    else:
        print('wtf man did you forget to use the targetinp function!!!')
    if url.endswith('/'):
        # This seemed preety ugly to me tbh
        url = list(url)
        url[-1] = ""
        url = "".join(url)
    tor = {'/','!','?','#','@','&','%','\\','*', ':'}
    for r in tor:
        url = url.replace(r, '_')
    return url

def getDataFromCmseek(url, token):

    reportFolder = init_result_dir(url)
    path = '/root/python_tool/CMSeeK/Result'
    reportPath = os.path.join(path, reportFolder)

    tsd, td, tsu = extract(url)
    domain = tsd + '.' + td + '.' + tsu
    domain = domain[1: len(domain)-1] if (domain[0] == '.' and domain[len(domain)-1] == '.') else domain[1:] if (domain[0] == '.') else domain[:len(domain)-1] if (domain[len(domain)-1] == '.') else domain

    if (domain == ''):
        return "Can not get data from cmseek", None
    
    if (token in pids_of_token.keys()):
        process = subprocess.Popen(['python','cmseek.py','-u',url,'--batch'], cwd='/root/python_tool/CMSeeK/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        pids_of_token[token].append(process.pid)
        process.wait()

        if (token in pids_of_token.keys()):
            pids_of_token[token].remove(process.pid)
            re, err = process.communicate()
            if (process.returncode != 1):
                return re, reportPath
            else:
                return "Can not get data from cmseek", None
        else:
            return "Can not get data from cmseek", None
    return "Can not get data from cmseek", None