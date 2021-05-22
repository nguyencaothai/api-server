import sys
sys.path.append('/root/python_tool/Sublist3r')
import sublist3r
from tldextract import extract

def getDataFromSublist3r(url):
    #Get domain name
    tsd, td, tsu = extract(url)
    url = td + '.' + tsu

    subdomains = sublist3r.main(url, 10, '', ports= None, silent=True, verbose= False, enable_bruteforce= False, engines=None)

    return subdomains
