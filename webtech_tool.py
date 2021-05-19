import webtech
import json

def getDataFromWebTech(url):

    wt = webtech.WebTech(options={'json': True, 'random-user-agent': True})

    try:
        report = wt.start_from_url(url)
        return report
    except:
        return ("Connection Error")