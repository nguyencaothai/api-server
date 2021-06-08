import whois
from tldextract import extract

def getDataFromWhois(url):
    #Get domain name
    tsd, td, tsu = extract(url)
    url = td + '.' + tsu
    
    try:
        info = whois.whois(url)
        return info
    except:
        return {
            "address": None, 
            "city": None, 
            "country": None, 
            "creation_date": None, 
            "dnssec": None, 
            "domain_name": None, 
            "emails": None, 
            "expiration_date": None, 
            "name": None, 
            "name_servers": None, 
            "org": None, 
            "referral_url": None, 
            "registrar": None, 
            "state": None, 
            "status": None, 
            "updated_date": None, 
            "whois_server": None, 
            "zipcode": None
        }