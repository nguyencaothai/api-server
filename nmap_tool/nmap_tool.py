import subprocess
import socket
from tldextract import extract
from pids import pids_of_token

def getDataFromNmap(url, token):
    #Convert domain to ip
    tsd, td, tsu = extract(url)
    url = tsd + '.' + td + '.' + tsu
    
    url = url[1: len(url)-1] if (url[0] == '.' and url[len(url)-1] == '.') else url[1:] if (url[0] == '.') else url[:len(url)-1] if (url[len(url)-1] == '.') else url

    if (url == ''):
        return "Can not get data from nmap"
    try:
        ip = socket.gethostbyname(url)
    except:
        return "Can not get data from nmap"
    
    reportNameTXT = 'nmap_' + token + '.report_1'
    reportNameXML = 'nmap_' + token + '.report_2'
    subprocess.run(['rm', reportNameTXT, reportNameXML], cwd='/root/python_tool/nmap_tool')

    #Run nmap with related ip
    if (token in pids_of_token.keys()):
        process = subprocess.Popen(['nmap','-A','-sV','-T4','-oN', reportNameTXT,'--script','vuln', '-oX', reportNameXML,ip], cwd='/root/python_tool/nmap_tool', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            pids_of_token[token].append(process.pid)
            process.wait()

            if (token in pids_of_token.keys()):
                pids_of_token[token].remove(process.pid)
                re, err = process.communicate()
                if (process.returncode != 1):
                    return "Success"
                else:
                    return "Can not get data from nmap"
            return "Can not get data from nmap"
        except:
            return "Can not get data from nmap"

    return "Can not get data from nmap"
