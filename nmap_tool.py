import subprocess
import socket
from tldextract import extract

def getDataFromNmap(url):
    #Convert domain to ip
    tsd, td, tsu = extract(url)
    url = tsd + '.' + td + '.' + tsu
    
    url = url[1: len(url)-1] if (url[0] == '.' and url[len(url)-1] == '.') else url[1:] if (url[0] == '.') else url[:len(url)-1] if (url[len(url)-1] == '.') else url

    # url = url.split('/')[2].replace('/','')
    try:
        ip = socket.gethostbyname(url)
    except:
        return "Can not get data from nmap"
        
    #Run nmap with related ip
    results = subprocess.run(['nmap','-A','-sV','-T4','-oN','nmap_results.txt','--script','vuln',ip], capture_output=True)

    if (results.returncode != 1):
        return (results.stdout)
    else:
        return "Can not get data from nmap"
