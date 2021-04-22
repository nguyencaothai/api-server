import flask
from flask import Response, request, jsonify
import re, os
import json, xmltodict

# local_modules

# Modules for web technologies scanning
from whatweb_tool import getDataFromWhatWeb
from webtech_tool import getDataFromWebTech

# Modules for subdomains scanning
from sublist3r_tool import getDataFromSublist3r

# Modules for directories/files scanning
from gobuster_tool import getDirsFromGobuster, getFilesFromGobuster

# Modules for domain information 
from whois_tool import getDataFromWhois

# Modules which related to DNS
from dig_tool import getDataFromDig

# Modules for Server scanning
from nmap_tool import getDataFromNmap

# Modules for WAF scanning
from wafw00f_tool import getDataFromWafw00f

# Modules for CMS scanning
from wpscan_tool import getDataFromWpscan
from droopescan_tool import getDataFromDroopescan
from joomscan_tool.joomscan_tool import getDataFromJoomscan
# from joomscan_tool.parseHTML import getJsonData

# Modules for Exploit DB
from searchsploit_tool import getDataFromSearchsploit

# Modules Web scanning with Nikto 
from nikto_tool import getDataFromNikto

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Web technologies scanning
@app.route('/api/v1/enumeration/whatweb', methods=['GET'])
def whatweb_api():
    if 'url' in request.args:
        #Get cookie if it is defined
        try:
            cookie = request.args['cookie']
        except:
            cookie = None
           
        results = getDataFromWhatWeb(request.args['url'], cookie)

        contents = {}
        contents['technologies'] = []

        if (results):

            with open('whatweb_results.xml', 'r') as f:
                data = xmltodict.parse(f.read())
                
                # In case wrong URL or nothing return
                if (data['log'] == None):
                    return jsonify(contents)
                else:

                    # Delete key:value which un-needed
                    try:
                        # In case having many targets
                        for i in range(0, len(data['log']['target'])):
                            contents['technologies'] = contents['technologies'] + data['log']['target'][i]['plugin']

                        # Remove duplicate technologies
                        res_list = []
                        for i in range(len(contents['technologies'])):
                            if contents['technologies'][i] not in contents['technologies'][i + 1:]:
                                res_list.append(contents['technologies'][i])
                        
                        # Assign res_list back again to contents
                        contents['technologies'] = res_list
                        return jsonify(contents)

                    except: 
                        # In case having only one target
                        contents['technologies'] = data['log']['target']['plugin']
                        return jsonify(contents)
        else:
            return jsonify(contents)
    else:
        return jsonify('Define url parameter')

@app.route('/api/v1/enumeration/webtech', methods=['GET'])
def webtech_api():
    if 'url' in request.args:
        # Check if URL has http|https
        rightFormat = re.search("^(http|https)://", request.args['url'])

        contents = {}
        contents['technologies'] = []

        if (rightFormat):
            results = getDataFromWebTech(request.args['url'])
            if (results != "Connection Error"):
                contents['technologies'] = results.pop('tech')
                return jsonify(contents)
            else:
                return jsonify(contents)
        else:
            return jsonify("Please add 'http' or 'https' to url parameter")
    else:
        return jsonify("Define url parameter")


# Subdomains scanning
@app.route('/api/v1/enumeration/sublist3r', methods=['GET'])
def sublist3r_api():
    if 'url' in request.args:

        results = {}
        results['subdomains'] = []

        subdomains = getDataFromSublist3r(request.args['url'])

        if (len(subdomains) != 0) :
            results = {}
            results['subdomains'] = list(subdomains)
            return jsonify(results)
        else:
            return jsonify(results)
    else:
        return jsonify('Define url parameter')


# Directories/files scanning
@app.route('/api/v1/enumeration/gobuster', methods=['GET'])
def gobuster_api():


    #Check whether requests have url parameter
    if 'url' in request.args:
        
        #Check whether url parameter in right format
        rightFormat = re.search("^(http|https)://", request.args['url'])

        #Get cookie if it is defined
        try:
            cookie = request.args['cookie']
        except:
            cookie = ""

        if (rightFormat):
            results_dirs = getDirsFromGobuster(request.args['url'], cookie)
            results_files = getFilesFromGobuster(request.args['url'], cookie)

            results = {}
            results['files'] = []
            results['directories'] = []

            if (results_dirs == 'wrong URL' and results_files == 'wrong URL'):
                return jsonify(results)

            else:
                if (results_dirs != 'wrong URL'):
                    data = []
                    directories = results_dirs.decode('UTF-8').strip().split('\n\r')
                    for directory in directories:
                        data.append(directory.strip())
                    results['directories'] = data

                if (results_files != 'wrong URL'):
                    data = []
                    files = results_files.decode('UTF-8').strip().split('\n\r')
                    for file in files:
                        data.append(file.strip())    
                    results['files'] = data

                return jsonify(results)
        else:
            return jsonify("Please add 'http' or 'https' to url parameter")
    else:
        return jsonify('Define url parameter')


# Domain information
@app.route('/api/v1/enumeration/whois', methods=['GET'])
def whois_api():
    if 'url' in request.args:
        info = getDataFromWhois(request.args['url'])
        return jsonify(info)
    else:
        return jsonify('Define url parameter')


# DNS information
@app.route('/api/v1/enumeration/dig', methods=['GET'])
def dig_api():

    if 'url' in request.args:

        contents = getDataFromDig(request.args['url'])
        return jsonify(contents)

    else:
        return jsonify('Please fill in a specific url')


# Server information
@app.route('/api/v1/enumeration/nmap', methods=['GET'])
def nmap_api():
    if 'url' in request.args:
        results = getDataFromNmap(request.args['url'])

        contents = ""

        if (results != "Can not get data from nmap"):
            with open('nmap_results.txt','r') as f:
                # Load to dictionary again for post-processing
                contents = f.read()   

                return contents
        else:
            return contents
    else:
        return jsonify('Define url parameter')


# WAF scanning
@app.route('/api/v1/enumeration/wafw00f', methods=['GET'])
def wafw00f_api():
    if 'url' in request.args:
        results = getDataFromWafw00f(request.args['url'])

        contents = {}
        contents['wafs'] = []

        if (results):
            with open('wafw00f.json','r') as f:
                tmp = json.loads(f.read())
                contents['wafs'] = tmp
                return jsonify(contents)
        else:
            return jsonify(contents)
    else:
        return jsonify('Define url parameter') 


# CMS scanning
@app.route('/api/v1/enumeration/wpscan', methods=['GET'])
def wpscan_api():
    if 'url' in request.args:

        #Check whether url parameter in right format
        rightFormat = re.search("^(http|https)://", request.args['url'])

        contents = {}
        
        if (rightFormat):

            #Get cookie if it is defined
            try:
                cookie = request.args['cookie']
            except:
                cookie = None

            results = getDataFromWpscan(request.args['url'], cookie)

            if (results):
                with open('wpscan.json', 'r') as f:
                    contents = json.loads(f.read())
                    return jsonify(contents)
            else:
                return jsonify(contents)
        else:
            return jsonify("Please add 'http' or 'https' to url parameter")
    else:
        return jsonify('Define url paramter')

@app.route('/api/v1/enumeration/droopescan', methods=['GET'])
def droopescan_api():
    if 'url' in request.args:

        results = getDataFromDroopescan(request.args['url'])
        
        contents = {}

        if (results != "Can not get data from droopescan"):
            try:
                contents = results.decode('utf-8')
                return jsonify(json.loads(contents))
            except:
                return jsonify({})
        else:
            return jsonify(contents)
    else:
        return jsonify('Define url paramter')

@app.route('/api/v1/enumeration/joomscan', methods=['GET'])
def joomscan_api():
    if 'url' in request.args:

        results = getDataFromJoomscan(request.args['url'])

        contents = ""

        if (results):

            # Get path of reports
            path = '/root/python_tool/joomscan/reports/'
            reportFolder = os.listdir(path)[0]
            reportPath = os.path.join(path, reportFolder)

            # Read contents in report with extension is txt
            for reportFile in os.listdir(reportPath):
                if re.search("(.txt)$", reportFile):

                    with open(os.path.join(reportPath, reportFile), 'r') as f:
                        contents = f.read()
                        return contents
        else:
            return contents
    
    else:
        return jsonify('Define url paramter')


# Search exploit from ExploitDB
@app.route('/api/v1/enumeration/searchsploit', methods=['GET'])
def searchsploit_api():

    path = 'https://www.exploit-db.com/raw/'

    if 'pattern' in request.args:
        results = getDataFromSearchsploit(request.args['pattern'])
        contents = {}
        contents['RESULTS_EXPLOIT'] = []

        if (results):
            with open('searchsploit_results.json', 'r') as f:
                contents = json.loads(f.read())

                # Delete un-needed elements
                contents.pop('SEARCH')
                contents.pop('DB_PATH_EXPLOIT')
                contents.pop('DB_PATH_SHELLCODE')
                contents.pop('RESULTS_SHELLCODE')
                
                for i in range(0, len(contents['RESULTS_EXPLOIT'])):
                    edb_id = contents['RESULTS_EXPLOIT'][i]['EDB-ID']
                    contents['RESULTS_EXPLOIT'][i].pop('EDB-ID')
                    contents['RESULTS_EXPLOIT'][i].pop('Path')
                    contents['RESULTS_EXPLOIT'][i]['URL'] = path + edb_id

                return jsonify(contents)
        else:
            return jsonify(jsonify)
    else:
        return jsonify('Define url paramter')
    
# Web scanning with Nikto      
@app.route('/api/v1/enumeration/nikto', methods=['GET'])  
def nikto_api():
    if 'url' in request.args:
        rightFormat = re.search("^(http|https)://", request.args['url'])

        contents = {}

        if (rightFormat):
            results = getDataFromNikto(request.args['url'])
            if (results):
                with open('nikto_results.json', 'r') as f:
                    contents = json.loads(f.read()[::-1].replace(',','',2)[::-1])
                    return jsonify(contents)
            else:
                return jsonify(contents)
        else:
            return jsonify("Please add 'http' or 'https' to url parameter")
    else:
        return jsonify('Define url paramter')

app.run(host='0.0.0.0', port=5000)
