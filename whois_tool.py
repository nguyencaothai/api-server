import whois
from tldextract import extract

def getDataFromWhois(url):
    #Get domain name
    tsd, td, tsu = extract(url)
    url = td + '.' + tsu
    
    info = whois.whois(url)
    return info