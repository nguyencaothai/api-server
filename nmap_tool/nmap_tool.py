import subprocess
import socket
from tldextract import extract

def getDataFromNmap(url, token):
    #Convert domain to ip
    tsd, td, tsu = extract(url)
    url = tsd + '.' + td + '.' + tsu
    
    url = url[1: len(url)-1] if (url[0] == '.' and url[len(url)-1] == '.') else url[1:] if (url[0] == '.') else url[:len(url)-1] if (url[len(url)-1] == '.') else url

    # url = url.split('/')[2].replace('/','')
    try:
        ip = socket.gethostbyname(url)
    except:
        return "Can not get data from nmap"
    
    reportNameTXT = 'nmap_' + token + '.report_1'
    reportNameXML = 'nmap_' + token + '.report_2'
    subprocess.run(['rm', reportNameTXT, reportNameXML], cwd='/root/python_tool/nmap_tool')

    #Run nmap with related ip
    results = subprocess.run(['nmap','-A','-sV','-T4','-oN', reportNameTXT,'--script','vuln', '-oX', reportNameXML,ip], capture_output=True, cwd='/root/python_tool/nmap_tool')

    if (results.returncode != 1):
        return (results.stdout)
    else:
        return "Can not get data from nmap"
